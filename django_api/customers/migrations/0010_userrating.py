# Generated by Django 5.0.3 on 2024-03-10 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_remove_account_is_verified_alter_account_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, '1 start'), (2, '2 starts'), (3, '3 starts'), (4, '4 starts'), (5, '5 starts')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creatorID', to=settings.AUTH_USER_MODEL)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userID', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('creator', 'userID')},
            },
        ),
    ]
