# Generated by Django 4.2.7 on 2023-12-01 18:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0004_task_input_file_task_output_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="constraints",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256),
                default=list,
                size=None,
            ),
        ),
    ]
