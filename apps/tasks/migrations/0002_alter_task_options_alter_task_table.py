# Generated by Django 4.2.5 on 2023-10-03 17:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={},
        ),
        migrations.AlterModelTable(
            name="task",
            table="tasks",
        ),
    ]
