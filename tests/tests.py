from django.test import TestCase
from .models import Person, Number, SSN, Group
from fkreplace import merge

class MergeTests(TestCase):
    def setUp(self):
        self.a = Person.objects.create(name='alf')
        self.b = Person.objects.create(name='bee')
        self.g = Group.objects.create(name='Team Awesome')

    def test_fk_simple(self):
        Number.objects.create(person=self.a, number='555-1111')
        Number.objects.create(person=self.a, number='555-1112')
        merge(self.a, self.b)
        # move FKs pointing at A to C
        assert self.a.numbers.count() == 0
        assert self.b.numbers.count() == 2
        assert Number.objects.count() == 2

    def test_fk_existing(self):
        Number.objects.create(person=self.a, number='555-1112')
        Number.objects.create(person=self.b, number='555-1113')
        merge(self.a, self.b)
        # everything now on B
        assert self.a.numbers.count() == 0
        assert self.b.numbers.count() == 2
        assert Number.objects.count() == 2

    def test_one2one_simple(self):
        SSN.objects.create(person=self.a, number='1')
        merge(self.a, self.b)
        # move FKs pointing at A to B
        #TODO: assert self.a.ssn is None
        assert Person.objects.get(pk=self.b.pk).ssn.number == '1'
        assert SSN.objects.count() == 1

    # TODO: test one2one when there's a conflict

    def test_many2many_simple(self):
        self.g.people.add(self.a)
        merge(self.a, self.b)
        # A's membership in G has been moved to B
        assert self.g.people.get().name == self.b.name
        assert self.a.groups.all().count() == 0
        assert self.b.groups.all().count() == 1

    def test_many2many_redundant(self):
        self.g.people.add(self.a)
        self.g.people.add(self.b)
        merge(self.a, self.b)
        # A's membership in G is redundant with B's
        assert self.g.people.all().count() == 1
        assert self.a.groups.all().count() == 0
        assert self.b.groups.all().count() == 1

    def test_many2many_same_class(self):
        f = Person.objects.create(name='friend')
        self.a.friends.add(f)
        merge(self.a, self.b)
        assert self.a.friends.all().count() == 0
        assert self.b.friends.get().name == f.name
        assert f.get().name == self.b.name
