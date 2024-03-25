# Generated by Django 5.0.3 on 2024-03-06 20:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_rename_logos_account_logo_alter_account_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(error_messages={'unique': "You've already registered"}, max_length=254, unique=True, validators=[django.core.validators.EmailValidator(allowlist=['lpnu.ua'], code=None, message='Incorrect email, check if it ends with: lpnu.ua, other university')]),
        ),
    ]