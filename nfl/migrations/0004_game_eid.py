# Generated by Django 2.1.1 on 2018-10-22 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0003_game_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='eid',
            field=models.IntegerField(default=0),
        ),
    ]
