# Generated by Django 4.1.1 on 2022-09-30 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('founded_at', models.CharField(max_length=50)),
                ('funding_rounds', models.CharField(max_length=50)),
                ('total_funding_usd', models.CharField(max_length=50)),
                ('milestones', models.CharField(max_length=50)),
                ('relationships', models.CharField(max_length=50)),
            ],
        ),
    ]
