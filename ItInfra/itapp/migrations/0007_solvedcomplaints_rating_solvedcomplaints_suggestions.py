# Generated by Django 4.1.5 on 2023-02-08 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itapp', '0006_solvedcomplaints'),
    ]

    operations = [
        migrations.AddField(
            model_name='solvedcomplaints',
            name='Rating',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='solvedcomplaints',
            name='suggestions',
            field=models.TextField(default='No Suggestions'),
        ),
    ]
