# -*- coding: utf-8 -*-

import copy
from datetime import date
from django.utils.functional import curry
from django.utils.translation import (ugettext_lazy as _, string_concat)
from django.utils.encoding import smart_unicode
from django.db.backends import util
from django.db import connection
from django import forms
from django.db.models.fields.related import (ForeignKey, router, QuerySet, ReverseSingleRelatedObjectDescriptor,
    RECURSIVE_RELATIONSHIP_CONSTANT, add_lazy_relation, ReverseManyRelatedObjectsDescriptor, RelatedField, Field,
    ManyToManyRel, ManyRelatedObjectsDescriptor)
from temporal.models.base import TemporalModel
from temporal.models.trail import TemporalTrail


class ReverseTemporalSingleRelatedObjectDescriptor(ReverseSingleRelatedObjectDescriptor):
    # This class provides the functionality that makes the related-object
    # managers available as attributes on a model class, for fields that have
    # a single "remote" value, on the class that defines the related field.
    # In the example "choice.poll", the poll attribute is a
    # ReverseSingleRelatedObjectDescriptor instance.

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        cache_name = self.field.get_cache_name()
        try:
            return getattr(instance, cache_name)
        except AttributeError:
            val = getattr(instance, self.field.attname)
            # default = date.today() to use with not temporal models
            actual_date = getattr(instance, '_actual_date', date.today())
            if val is None:
                # If NULL is an allowed value, return it.
                if self.field.null:
                    return None
                raise self.field.rel.to.DoesNotExist
            other_field = self.field.rel.get_related_field()
            if other_field.rel:
                params = {'%s__pk' % self.field.rel.field_name: val}
            else:
                params = {'%s__exact' % self.field.rel.field_name: val}

            # If the related manager indicates that it should be used for
            # related fields, respect that.
            rel_mgr = self.field.rel.to._default_manager
            db = router.db_for_read(self.field.rel.to, instance=instance)
            if getattr(rel_mgr, 'use_for_related_fields', False):
                rel_obj = rel_mgr.using(db).get(**params)
            else:
                rel_obj = QuerySet(self.field.rel.to).using(db).get(**params)

            if actual_date:
                rel_obj = rel_obj.history.get_actual(actual_date)
                # that choice.poll.TYPE could be actual 
                rel_obj._actual_date = actual_date
                
            setattr(instance, cache_name, rel_obj)
            return rel_obj


class TemporalForeignKey(ForeignKey):

    def contribute_to_class(self, cls, name):
        super(TemporalForeignKey, self).contribute_to_class(cls, name)
        setattr(cls, self.name, ReverseTemporalSingleRelatedObjectDescriptor(self))
        if isinstance(self.rel.to, basestring):
            target = self.rel.to
        else:
            target = self.rel.to._meta.db_table
        cls._meta.duplicate_targets[self.column] = (target, "o2m")

#    TODO: write ForeignTemporalRelatedObjectsDescriptor if needed
#    def contribute_to_related_class(self, cls, related):
#        # Internal FK's - i.e., those with a related name ending with '+' -
#        # don't get a related descriptor.
#        if not self.rel.is_hidden():
#            setattr(cls, related.get_accessor_name(), ForeignTemporalRelatedObjectsDescriptor(related))
#            if self.rel.limit_choices_to:
#                cls._meta.related_fkey_lookups.append(self.rel.limit_choices_to)
#        if self.rel.field_name is None:
#            self.rel.field_name = cls._meta.pk.name


def create_many_to_many_intermediary_model(field, klass):
    from django.db import models
    managed = True
    if isinstance(field.rel.to, basestring) and field.rel.to != RECURSIVE_RELATIONSHIP_CONSTANT:
        to_model = field.rel.to
        to = to_model.split('.')[-1]
        def set_managed(field, model, cls):
            field.rel.through._meta.managed = model._meta.managed or cls._meta.managed
        add_lazy_relation(klass, field, to_model, set_managed)
    elif isinstance(field.rel.to, basestring):
        to = klass._meta.object_name
        to_model = klass
        managed = klass._meta.managed
    else:
        to = field.rel.to._meta.object_name
        to_model = field.rel.to
        managed = klass._meta.managed or to_model._meta.managed
    name = '%s_%s' % (klass._meta.object_name, field.name)
    if field.rel.to == RECURSIVE_RELATIONSHIP_CONSTANT or to == klass._meta.object_name:
        from_ = 'from_%s' % to.lower()
        to = 'to_%s' % to.lower()
    else:
        from_ = klass._meta.object_name.lower()
        to = to.lower()
    meta = type('Meta', (object,), {
        'db_table': field._get_m2m_db_table(klass._meta),
        'managed': managed,
        'auto_created': klass,
        'app_label': klass._meta.app_label,
        'unique_together': (from_, to, 'date_begin'),
        'verbose_name': '%(from)s-%(to)s relationship' % {'from': from_, 'to': to},
        'verbose_name_plural': '%(from)s-%(to)s relationships' % {'from': from_, 'to': to},
    })
    # Construct and return the new class.
    return type(name, (models.Model,), {
#    return type(name, (TemporalModel,), {
        'Meta': meta,
        '__module__': klass.__module__,
        'history': TemporalTrail(),
        from_: models.ForeignKey(klass, related_name='%s+' % name),
        to: models.ForeignKey(to_model, related_name='%s+' % name)
    })


class TemporalManyToManyField(RelatedField, Field):
    description = _("Many-to-many relationship")
    def __init__(self, to, **kwargs):
        try:
            assert not to._meta.abstract, "%s cannot define a relation with abstract class %s" % (self.__class__.__name__, to._meta.object_name)
        except AttributeError: # to._meta doesn't exist, so it must be RECURSIVE_RELATIONSHIP_CONSTANT
            assert isinstance(to, basestring), "%s(%r) is invalid. First parameter to ManyToManyField must be either a model, a model name, or the string %r" % (self.__class__.__name__, to, RECURSIVE_RELATIONSHIP_CONSTANT)

        kwargs['verbose_name'] = kwargs.get('verbose_name', None)
        kwargs['rel'] = ManyToManyRel(to,
            related_name=kwargs.pop('related_name', None),
            limit_choices_to=kwargs.pop('limit_choices_to', None),
            symmetrical=kwargs.pop('symmetrical', to==RECURSIVE_RELATIONSHIP_CONSTANT),
            through=kwargs.pop('through', None))

        self.db_table = kwargs.pop('db_table', None)
        if kwargs['rel'].through is not None:
            assert self.db_table is None, "Cannot specify a db_table if an intermediary model is used."

        Field.__init__(self, **kwargs)

        msg = _('Hold down "Control", or "Command" on a Mac, to select more than one.')
        self.help_text = string_concat(self.help_text, ' ', msg)

    def get_choices_default(self):
        return Field.get_choices(self, include_blank=False)

    def _get_m2m_db_table(self, opts):
        "Function that can be curried to provide the m2m table name for this relation"
        if self.rel.through is not None:
            return self.rel.through._meta.db_table
        elif self.db_table:
            return self.db_table
        else:
            return util.truncate_name('%s_%s' % (opts.db_table, self.name),
                                      connection.ops.max_name_length())

    def _get_m2m_attr(self, related, attr):
        "Function that can be curried to provide the source accessor or DB column name for the m2m table"
        cache_attr = '_m2m_%s_cache' % attr
        if hasattr(self, cache_attr):
            return getattr(self, cache_attr)
        for f in self.rel.through._meta.fields:
            if hasattr(f,'rel') and f.rel and f.rel.to == related.model:
                setattr(self, cache_attr, getattr(f, attr))
                return getattr(self, cache_attr)

    def _get_m2m_reverse_attr(self, related, attr):
        "Function that can be curried to provide the related accessor or DB column name for the m2m table"
        cache_attr = '_m2m_reverse_%s_cache' % attr
        if hasattr(self, cache_attr):
            return getattr(self, cache_attr)
        found = False
        for f in self.rel.through._meta.fields:
            if hasattr(f,'rel') and f.rel and f.rel.to == related.parent_model:
                if related.model == related.parent_model:
                    # If this is an m2m-intermediate to self,
                    # the first foreign key you find will be
                    # the source column. Keep searching for
                    # the second foreign key.
                    if found:
                        setattr(self, cache_attr, getattr(f, attr))
                        break
                    else:
                        found = True
                else:
                    setattr(self, cache_attr, getattr(f, attr))
                    break
        return getattr(self, cache_attr)

    def value_to_string(self, obj):
        data = ''
        if obj:
            qs = getattr(obj, self.name).all()
            data = [instance._get_pk_val() for instance in qs]
        else:
            # In required many-to-many fields with only one available choice,
            # select that one available choice.
            if not self.blank:
                choices_list = self.get_choices_default()
                if len(choices_list) == 1:
                    data = [choices_list[0][0]]
        return smart_unicode(data)

    def contribute_to_class(self, cls, name):
        # To support multiple relations to self, it's useful to have a non-None
        # related name on symmetrical relations for internal reasons. The
        # concept doesn't make a lot of sense externally ("you want me to
        # specify *what* on my non-reversible relation?!"), so we set it up
        # automatically. The funky name reduces the chance of an accidental
        # clash.
        if self.rel.symmetrical and (self.rel.to == "self" or self.rel.to == cls._meta.object_name):
            self.rel.related_name = "%s_rel_+" % name

        super(TemporalManyToManyField, self).contribute_to_class(cls, name)

        # The intermediate m2m model is not auto created if:
        #  1) There is a manually specified intermediate, or
        #  2) The class owning the m2m field is abstract.
        if not self.rel.through and not cls._meta.abstract:
            self.rel.through = create_many_to_many_intermediary_model(self, cls)

        # Add the descriptor for the m2m relation
        setattr(cls, self.name, ReverseManyRelatedObjectsDescriptor(self))

        # Set up the accessor for the m2m table name for the relation
        self.m2m_db_table = curry(self._get_m2m_db_table, cls._meta)

        # Populate some necessary rel arguments so that cross-app relations
        # work correctly.
        if isinstance(self.rel.through, basestring):
            def resolve_through_model(field, model, cls):
                field.rel.through = model
            add_lazy_relation(cls, self, self.rel.through, resolve_through_model)

        if isinstance(self.rel.to, basestring):
            target = self.rel.to
        else:
            target = self.rel.to._meta.db_table
        cls._meta.duplicate_targets[self.column] = (target, "m2m")

    def contribute_to_related_class(self, cls, related):
        # Internal M2Ms (i.e., those with a related name ending with '+')
        # don't get a related descriptor.
        if not self.rel.is_hidden():
            setattr(cls, related.get_accessor_name(), ManyRelatedObjectsDescriptor(related))

        # Set up the accessors for the column names on the m2m table
        self.m2m_column_name = curry(self._get_m2m_attr, related, 'column')
        self.m2m_reverse_name = curry(self._get_m2m_reverse_attr, related, 'column')

        self.m2m_field_name = curry(self._get_m2m_attr, related, 'name')
        self.m2m_reverse_field_name = curry(self._get_m2m_reverse_attr, related, 'name')

        get_m2m_rel = curry(self._get_m2m_attr, related, 'rel')
        self.m2m_target_field_name = lambda: get_m2m_rel().field_name
        get_m2m_reverse_rel = curry(self._get_m2m_reverse_attr, related, 'rel')
        self.m2m_reverse_target_field_name = lambda: get_m2m_reverse_rel().field_name

    def set_attributes_from_rel(self):
        pass

    def value_from_object(self, obj):
        "Returns the value of this field in the given model instance."
        return getattr(obj, self.attname).all()

    def save_form_data(self, instance, data):
        setattr(instance, self.attname, data)

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {
            'form_class': forms.ModelMultipleChoiceField,
            'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to)
        }
        defaults.update(kwargs)
        # If initial is passed in, it's a list of related objects, but the
        # MultipleChoiceField takes a list of IDs.
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if callable(initial):
                initial = initial()
            defaults['initial'] = [i._get_pk_val() for i in initial]
        return super(TemporalManyToManyField, self).formfield(**defaults)

    def db_type(self, connection):
        # A ManyToManyField is not represented by a single column,
        # so return None.
        return None

try:    
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([],
#                            (
#            (
#                (TemporalForeignKey,),
#                [],
#                {
#                    "to": ["rel.to", {}],
#                    "to_field": ["rel.field_name", {"default_attr": "rel.to._meta.pk.name"}],
#                    "related_name": ["rel.related_name", {"default": None}],
#                    "db_index": ["db_index", {"default": True}],
#                },
#            ),
#            (
#                (TemporalManyToManyField,),
#                [],
#                {
#                    "to": ["rel.to", {}],
#                    "symmetrical": ["rel.symmetrical", {"default": True}],
#                    "related_name": ["rel.related_name", {"default": None}],
#                    "db_table": ["db_table", {"default": None}],
#                    # TODO: Kind of ugly to add this one-time-only option
#                    "through": ["rel.through", {"ignore_if_auto_through": True}],
#                },
#            ),
#        ),                            
        ("^temporal\.models\.fields\.TemporalForeignKey", "^temporal\.models\.fields\.TemporalManyToManyField",)
    )
except:
    pass
