# Generated by Django 5.0.6 on 2024-05-24 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='mode',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
