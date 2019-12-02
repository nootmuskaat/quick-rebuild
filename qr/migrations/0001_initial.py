# Generated by Django 2.1.13 on 2019-10-21 10:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Builds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sha', models.CharField(max_length=40, unique=True, validators=[django.core.validators.RegexValidator('^[a-z0-9]{40}$')])),
                ('project', models.CharField(max_length=20)),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ECL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^ENV_VER_[A-Z0-9]+_[0-9]{4}_[0-9]{6}_[0-9]{6}$')])),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='builds',
            name='ecl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='qr.ECL'),
        ),
        migrations.AddField(
            model_name='builds',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='qr.Job'),
        ),
        migrations.AddField(
            model_name='builds',
            name='sha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='builds', to='qr.Commit'),
        ),
        migrations.AlterUniqueTogether(
            name='builds',
            unique_together={('sha', 'job', 'ecl')},
        ),
    ]