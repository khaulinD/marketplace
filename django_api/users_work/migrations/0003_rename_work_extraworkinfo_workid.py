# Generated by Django 5.0.3 on 2024-03-14 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_work', '0002_rename_resume_extraworkinfo_work'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extraworkinfo',
            old_name='work',
            new_name='workID',
        ),
    ]
