# Generated by Django 3.2.3 on 2021-06-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box4bet', '0003_rename_confirmed_odd_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='odds_locked',
            field=models.BooleanField(default=False),
        ),
    ]