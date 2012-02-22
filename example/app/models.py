from temporal.models import models, TemporalForeignKey, TemporalModel, TemporalTrail

class Person(TemporalModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    salary = models.PositiveIntegerField()
    organization = TemporalForeignKey('Organization')
    
    history = TemporalTrail()

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)
        
class Organization(TemporalModel):
    name = models.CharField(max_length=255)
    
    history = TemporalTrail()

    def __str__(self):
        return u"%s" % (self.name)
