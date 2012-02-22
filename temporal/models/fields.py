from datetime import date
from django.db.models.fields.related import (ForeignKey, router, QuerySet, ReverseSingleRelatedObjectDescriptor)


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
