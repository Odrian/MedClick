# Generated by Django 3.2 on 2021-06-12 21:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('key', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=16)),
                ('last_activity', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
