from django.test import TestCase
from .models import Person, Number, SSN, Group
from fkreplace import merge

class MergeTests(TestCase):
    def setUp(self):
        self.a = Person.objects.create(name='alf')
        self.b = Person.objects.create(name='bee')
        self.c = Person.objects.create(name='sea')
        Number.objects.create(person=self.a, number='555-1111')
        Number.objects.create(person=self.a, number='555-1112')
        Number.objects.create(person=self.b, number='555-1113')
        SSN.objects.create(person=self.a, number='1')
        SSN.objects.create(person=self.b, number='2')
        self.g = Group.objects.create(name='Team Awesome')
        self.g.people.add(self.a)
        self.g.people.add(self.b)

    def test_fk_simple(self):
        merge(self.a, self.c)
        # move FKs pointing at A to C
        assert self.a.numbers.count() == 0
        assert self.c.numbers.count() == 2
        assert Number.objects.count() == 3

    def test_fk_existing(self):
        merge(self.a, self.b)
        # everything now on b
        assert self.a.numbers.count() == 0
        assert self.b.numbers.count() == 3
        assert Number.objects.count() == 3

    def test_one2one_simple(self):
        merge(self.a, self.c)
        # move FKs pointing at A to C
        #assert self.a.ssn is None
        c = Person.objects.get(pk=self.c.pk)
        c.ssn.number == 1
        assert SSN.objects.count() == 2

    # TODO: test one2one when there's a conflict

    def test_many2many_simple(self):
        merge(self.a, self.c)
        # A's membership in G has been moved to C
        assert self.g.people.all().count() == 2
        assert self.a.groups.all().count() == 0
        assert self.c.groups.all().count() == 1

    def test_many2many_redundant(self):
        merge(self.a, self.b)
        # A's membership in G is redundant with B's
        assert self.g.people.all().count() == 1
        assert self.a.groups.all().count() == 0
        assert self.b.groups.all().count() == 1

    def test_many2many_self(self):
        self.a.friends.add(self.b)
        merge(self.a, self.c)
        import pdb; pdb.set_trace()
        assert self.a.friends.all().count() == 0
        assert self.b.friends.get().name == self.c
        assert self.c.friends.get().name == self.b
