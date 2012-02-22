======================
Django-temporal-models
======================

Django-temporal-models это темпоральные модели навеянные 1совскими регистрами сведений.

Небольшой пример
==============
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

	...
	    
	>>> from app.models import Organization, Person
	>>> from datetime import date
	>>>
	>>>	org = Organization.objects.create(name=u'Муниципальное унитарное предприятие городского транспорта "Тюменьгортранс"', date_begin=date(1997, 01, 31))
	>>>
	>>> org.name = u'Муниципальное учреждение пассажирского городского транспорта "Тюменьгортранс"'
	>>> org.date_begin = date(2004,7,1)
	>>> org.save()
	>>>
	>>> org.name = u'Муниципальное казенное учреждение "Тюменьгортранс"'
	>>> org.date_begin = date(2012,1,11)
	>>> org.save()
	>>>
	>>> org.get_actual(date(2010,1,1))
	<OrganizationTemporal: Муниципальное учреждение пассажирского городского транспорта "Тюменьгортранс" as of 2004-07-01..2012-01-10>
	>>>
	>>> person = Person.objects.create(first_name=u'Василий', last_name=u'Пупкин', salary=7000, organization=org, date_begin=date(2000,5,10))
	>>>	
	>>> person.date_begin=date(2005,1,1)
	>>> person.salary=12000
	>>> person.save()
	>>>
	>>> person.date_begin=date(2010,1,1)
	>>> person.salary=17000
	>>> person.save()
	>>>
	>>> person.date_begin=date(2012,2,1)
	>>> person.salary=20000
	>>> person.save()
	>>>
	>>> person.get_actual()
	<PersonTemporal: Василий Пупкин as of 2012-02-01..>
	>>> 
	>>> person.get_actual().organization
	<OrganizationTemporal: Муниципальное казенное учреждение "Тюменьгортранс" as of 2012-01-11..>
	>>> 
	>>> person.get_actual(date(2011,10,1))
	<PersonTemporal: Василий Пупкин as of 2010-01-01..2012-01-31>
	>>>
	>>> person.get_actual(date(2011,10,1)).organization
	<OrganizationTemporal: Муниципальное учреждение пассажирского городского транспорта "Тюменьгортранс" as of 2004-07-01..2012-01-10>
