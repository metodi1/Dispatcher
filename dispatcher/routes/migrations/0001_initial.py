# Generated by Django 5.0.6 on 2024-10-19 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoundDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.CharField(max_length=100)),
                ('start_round', models.CharField(max_length=100)),
                ('end_round', models.CharField(max_length=100)),
                ('stops_round', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]