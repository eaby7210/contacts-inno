# Generated by Django 5.1.7 on 2025-03-19 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthtoken',
            name='access_token',
            field=models.CharField(max_length=600),
        ),
    ]
