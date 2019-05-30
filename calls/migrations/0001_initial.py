# Generated by Django 2.2.1 on 2019-05-29 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_id', models.IntegerField(unique=True, verbose_name='Unique call identifier')),
                ('start_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Start time of the call')),
                ('stop_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Stop time of the call')),
                ('source', models.CharField(blank=True, max_length=11, null=True, verbose_name='Call Source')),
                ('destination', models.CharField(blank=True, max_length=11, null=True, verbose_name='Call Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('start', 'Start'), ('stop', 'Stop')], max_length=5, verbose_name='Call type')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp of the call')),
                ('call_id', models.IntegerField(verbose_name='Unique call pair identifier')),
                ('source', models.CharField(blank=True, max_length=11, null=True, verbose_name='Call Source')),
                ('destination', models.CharField(blank=True, max_length=11, null=True, verbose_name='Call Destination')),
            ],
        ),
    ]