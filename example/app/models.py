from temporal.models import (models, TemporalForeignKey, TemporalModel, TemporalTrail,
                             TemporalManyToManyField)

class Person(TemporalModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    salary = models.PositiveIntegerField()
    organization = TemporalForeignKey('Organization')
#    groups = TemporalManyToManyField('Group', through='PersonGroup', null=True)
    groups = TemporalManyToManyField('Group', through='PersonGroup')
#    groups = models.ManyToManyField('Group', through='PersonGroup')
    
    history = TemporalTrail()

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)
        
class Organization(TemporalModel):
    name = models.CharField(max_length=255)
    
    history = TemporalTrail()

    def __str__(self):
        return u"%s" % (self.name)

class Group(TemporalModel):
    name = models.CharField(max_length=255)
    
    history = TemporalTrail()

    def __str__(self):
        return u"%s" % (self.name)

class PersonGroup(TemporalModel):
    person = TemporalForeignKey(Person)
    group = TemporalForeignKey(Group)

    history = TemporalTrail()
    
    class Meta:
        unique_together = ('person', 'group', 'date_begin')
