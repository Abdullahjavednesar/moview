# Generated by Django 2.2.3 on 2019-07-25 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20190722_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actor',
            field=models.ManyToManyField(blank=True, related_name='movie', through='movie.ActMovRel', to='movie.Actor'),
        ),
    ]
