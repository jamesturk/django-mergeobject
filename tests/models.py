from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    friends = models.ManyToManyField('self')


class Number(models.Model):
    person = models.ForeignKey(Person, related_name='numbers')
    number = models.CharField(max_length=10)


class SSN(models.Model):
    person = models.OneToOneField(Person, related_name='ssn')
    number = models.CharField(max_length=10)


class Group(models.Model):
    name = models.CharField(max_length=100)
    people = models.ManyToManyField(Person, related_name='groups')
