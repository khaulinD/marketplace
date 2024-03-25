# Generated by Django 5.0.3 on 2024-03-14 21:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_resume', '0002_extraresumeinfo_rename_extrainfo_resume_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraresumeinfo',
            name='resume',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='extra_info', serialize=False, to='users_resume.resume'),
        ),
    ]
