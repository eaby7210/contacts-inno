# Generated by Django 5.1.7 on 2025-03-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('country', models.CharField(max_length=10)),
                ('location_id', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('lead', 'Lead'), ('customer', 'Customer')], max_length=20)),
                ('date_added', models.DateTimeField()),
                ('date_updated', models.DateTimeField()),
                ('dnd', models.BooleanField(default=False)),
            ],
        ),
    ]
