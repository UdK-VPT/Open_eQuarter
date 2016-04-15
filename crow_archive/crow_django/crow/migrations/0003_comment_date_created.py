# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crow', '0002_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
