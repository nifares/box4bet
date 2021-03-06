# Generated by Django 2.2.6 on 2021-05-17 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('region', models.CharField(default='UNK', max_length=100)),
                ('entry_fee', models.IntegerField(null=True)),
                ('fee_currency', models.CharField(default='CBL', max_length=3)),
                ('betfair_id', models.BigIntegerField(unique=True)),
                ('enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('betfair_id', models.BigIntegerField(unique=True)),
                ('enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('home', models.CharField(max_length=100)),
                ('away', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('home_score', models.IntegerField(null=True)),
                ('home_score_90', models.IntegerField(null=True)),
                ('away_score', models.IntegerField(null=True)),
                ('away_score_90', models.IntegerField(null=True)),
                ('locked', models.BooleanField(default=False)),
                ('live', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('betfair_id', models.BigIntegerField(unique=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='box4bet.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='box4bet.Competition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Odd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('prize', models.FloatField(null=True)),
                ('winner', models.BooleanField(default=False)),
                ('betfair_id', models.BigIntegerField()),
                ('betfair_name', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='box4bet.Event')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='box4bet.CompetitionKind'),
        ),
        migrations.AddConstraint(
            model_name='odd',
            constraint=models.UniqueConstraint(fields=('event', 'betfair_id'), name='unique_betfair_id_event'),
        ),
    ]
