# Generated by Django 5.0.6 on 2024-05-24 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_session_mode_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('info', models.CharField(max_length=300)),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.mode')),
            ],
        ),
    ]
