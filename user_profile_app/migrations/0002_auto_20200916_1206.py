# Generated by Django 3.1.1 on 2020-09-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='completed_todos',
            field=models.IntegerField(default=0),
        ),
    ]
