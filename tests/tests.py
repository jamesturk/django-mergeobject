from django.test import TestCase
from .models import Person, Number, SSN

def setUp():
    a = Person.objects.create(name='alf')
    b = Person.objects.create(name='bee')
    Number.objects.create(person=a, number='123')
    Number.objects.create(person=a, number='1234')
