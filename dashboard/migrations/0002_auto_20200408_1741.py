# Generated by Django 3.0.4 on 2020-04-08 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dashboard_countries',
            field=models.CharField(blank=True, max_length=9999),
        ),
    ]