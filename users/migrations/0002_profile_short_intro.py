# Generated by Django 3.2.6 on 2021-09-18 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='short_intro',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='short intro'),
        ),
    ]
