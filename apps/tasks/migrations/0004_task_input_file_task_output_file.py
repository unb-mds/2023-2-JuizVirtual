# Generated by Django 4.2.7 on 2023-11-26 21:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_task_memory_limit_task_score_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="input_file",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="task",
            name="output_file",
            field=models.TextField(default=""),
        ),
    ]
