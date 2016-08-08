# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cor_role_user_depart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cor_Rule_Power',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_5', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cor_user_Power',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cor_User_Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, unique=True, null=True)),
                ('level', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
                ('superior_department', models.ForeignKey(blank=True, to='manager.Department', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail', models.EmailField(max_length=254, null=True, blank=True)),
                ('password', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_5', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
                ('DepartmentID', models.ForeignKey(blank=True, to='manager.Department', null=True)),
                ('superior_role', models.ForeignKey(blank=True, to='manager.Roles', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('temp_1', models.CharField(max_length=32, null=True)),
                ('temp_5', models.CharField(max_length=32, null=True)),
                ('temp_2', models.CharField(max_length=32, null=True)),
                ('temp_3', models.CharField(max_length=32, null=True)),
                ('temp_4', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Third_project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cor_user_rule',
            name='RuleID',
            field=models.ForeignKey(blank=True, to='manager.Rule', null=True),
        ),
        migrations.AddField(
            model_name='cor_user_rule',
            name='UserID',
            field=models.ForeignKey(related_name='rule_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='cor_user_power',
            name='PowerID',
            field=models.ForeignKey(blank=True, to='manager.Power', null=True),
        ),
        migrations.AddField(
            model_name='cor_user_power',
            name='UserID',
            field=models.ForeignKey(related_name='power_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='cor_rule_power',
            name='PowerID',
            field=models.ForeignKey(blank=True, to='manager.Power', null=True),
        ),
        migrations.AddField(
            model_name='cor_rule_power',
            name='RuleID',
            field=models.ForeignKey(blank=True, to='manager.Rule', null=True),
        ),
        migrations.AddField(
            model_name='cor_role_user_depart',
            name='RoleID',
            field=models.ForeignKey(blank=True, to='manager.Roles', null=True),
        ),
        migrations.AddField(
            model_name='cor_role_user_depart',
            name='UserID',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, max_length=32, null=True),
        ),
    ]
