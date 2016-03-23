# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('author', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='OeQLayer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('gml_id', models.CharField(null=True, max_length=254)),
                ('spatial_na', models.CharField(null=True, max_length=254)),
                ('spatial_al', models.CharField(null=True, max_length=254)),
                ('spatial_ty', models.CharField(null=True, max_length=254)),
                ('bld_id', models.CharField(null=True, max_length=254)),
                ('area', models.FloatField(null=True)),
                ('perimeter', models.FloatField(null=True)),
                ('yoc', models.FloatField(null=True)),
                ('pdens', models.FloatField(null=True)),
                ('floors', models.FloatField(null=True)),
                ('wn_ar', models.FloatField(null=True)),
                ('rf_ar', models.FloatField(null=True)),
                ('wl_com', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
                ('wl_ar', models.FloatField(null=True)),
                ('width', models.FloatField(null=True)),
                ('length', models.FloatField(null=True)),
                ('bs_ar', models.FloatField(null=True)),
                ('wn_rat', models.FloatField(null=True)),
                ('liv_ar', models.FloatField(null=True)),
                ('hhrs', models.FloatField(null=True)),
                ('bs_uc', models.FloatField(null=True)),
                ('rf_uc', models.FloatField(null=True)),
                ('wl_uc', models.FloatField(null=True)),
                ('wn_uc', models.FloatField(null=True)),
                ('bs_up', models.FloatField(null=True)),
                ('rf_up', models.FloatField(null=True)),
                ('wl_up', models.FloatField(null=True)),
                ('wn_up', models.FloatField(null=True)),
                ('bs_qtc', models.FloatField(null=True)),
                ('rf_qtc', models.FloatField(null=True)),
                ('wl_qtc', models.FloatField(null=True)),
                ('wn_qtc', models.FloatField(null=True)),
                ('bs_qtp', models.FloatField(null=True)),
                ('rf_qtp', models.FloatField(null=True)),
                ('wl_qtp', models.FloatField(null=True)),
                ('wn_qtp', models.FloatField(null=True)),
                ('bs_sqtc', models.FloatField(null=True)),
                ('rf_sqtc', models.FloatField(null=True)),
                ('wl_sqtc', models.FloatField(null=True)),
                ('wn_sqtc', models.FloatField(null=True)),
                ('bs_sqtp', models.FloatField(null=True)),
                ('rf_sqtp', models.FloatField(null=True)),
                ('wl_sqtp', models.FloatField(null=True)),
                ('wn_sqtp', models.FloatField(null=True)),
                ('achl', models.FloatField(null=True)),
                ('avr', models.FloatField(null=True)),
                ('hlac', models.FloatField(null=True)),
                ('hlap', models.FloatField(null=True)),
                ('htc', models.FloatField(null=True)),
                ('htp', models.FloatField(null=True)),
                ('ahdc', models.FloatField(null=True)),
                ('ahdp', models.FloatField(null=True)),
                ('solhel', models.FloatField(null=True)),
                ('solar', models.FloatField(null=True)),
                ('solhe', models.FloatField(null=True)),
                ('solcrt', models.FloatField(null=True)),
                ('soliar', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('layer', models.ForeignKey(null=True, to='crow.Layer')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='layer',
            field=models.ForeignKey(to='crow.Layer'),
        ),
    ]
