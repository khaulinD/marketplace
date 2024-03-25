# Generated by Django 5.0.3 on 2024-03-14 21:42

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField(default=0)),
                ('creatorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraWorkInfo',
            fields=[
                ('resume', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='extra_info', serialize=False, to='users_work.userwork')),
                ('work_course_lvl', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
                ('work_subject_name', models.CharField(max_length=50)),
                ('work_subject_teacher', models.CharField(max_length=50)),
            ],
        ),
    ]
