# Generated by Django 3.0.4 on 2020-04-17 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_profile_dashboard_states'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dashboard_date_range',
            field=models.CharField(blank=True, max_length=9999),
        ),
    ]
