# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet as QuerySet
from django.contrib.auth.models import User

from django.db.models import Q
from django.db import transaction
from datetime import date

from temporal.models.fields import TemporalForeignKey
from temporal.models.trail import TemporalTrail


class FakeDeleteQuerySet(QuerySet):
    ' QuerySet, не удаляющий данные физически '
    
    def delete(self):
        self.update(**{'deleted': True})
    delete.alters_data = True


class ActualManager(models.GeoManager):
    ' Менеджер актуальных записей '
    
    def get_query_set(self):
        return FakeDeleteQuerySet(self.model, using=self._db).filter(deleted=False)

    def get_plain_queryset(self):
        return QuerySet(self.model, using=self._db)


class ActualModel(models.Model):
    ' Модель для актуальных данных '
    
    # Поле для пометки актуальных записей.
    # Если запись уже не актуальна - она не удаляется физически, а лишь помечается как неактивная
    deleted = models.BooleanField(u'Удален', default=False, editable=False)

    # По-умолчанию будут выдаваться только актуальные записи
    # Порядок важен! _default_manager - это первый объявленный менеджер
    objects = ActualManager()

    def delete(self, *args, **kwargs):
        '''
        fake delete
        '''
        real_delete = kwargs.pop('real_delete', False)
        if not real_delete:
            self.deleted = True
            self.save()
        else:
            super(ActualModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class TemporalModel(ActualModel):
    '''
    Модель для темпоральных данных.
    '''

    date_begin = models.DateTimeField();
    date_end = models.DateTimeField(null=True, blank=True, editable=False);

    def save(self, *args, **kwargs):
        with transaction.commit_manually():
            try:
                super(TemporalModel, self).save(*args, **kwargs)
            except:
                transaction.rollback()
                raise
            else:
                transaction.commit()

    def delete(self, *args, **kwargs):
        self.date_begin = kwargs.pop('date_delete', date.today()) 
        with transaction.commit_manually():
            try:
                if kwargs.get('real_delete', False):
                    self.history.all().delete()
                super(TemporalModel, self).delete(*args, **kwargs)
            except:
                transaction.rollback()
                raise
            else:
                transaction.commit()

    def get_actual(self, actual_date=None):
        return self.history.get_actual(actual_date)

    class Meta:
        unique_together = ("id", "date_begin")
        abstract = True
