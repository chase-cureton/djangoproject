# Generated by Django 2.1.1 on 2018-10-25 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0006_game_offense_stats_longest_rush'),
    ]

    operations = [
        migrations.AddField(
            model_name='game_offense_stats',
            name='longest_rec',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game_offense_stats',
            name='longest_rec_td',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game_offense_stats',
            name='longest_rush_td',
            field=models.IntegerField(default=0),
        ),
    ]
