# Generated by Django 5.0.3 on 2024-03-09 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_account_user_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(error_messages={'unique': "You've already registered"}, max_length=254, unique=True),
        ),
    ]