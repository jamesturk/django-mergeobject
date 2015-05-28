# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('friends', models.ManyToManyField(to='tests.Person', related_name='friends_rel_+')),
            ],
        ),
        migrations.CreateModel(
            name='SSN',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.CharField(max_length=10)),
                ('person', models.OneToOneField(to='tests.Person')),
            ],
        ),
        migrations.AddField(
            model_name='number',
            name='person',
            field=models.ForeignKey(to='tests.Person', related_name='numbers'),
        ),
        migrations.AddField(
            model_name='group',
            name='people',
            field=models.ManyToManyField(to='tests.Person'),
        ),
    ]
