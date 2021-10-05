# Generated by Django 3.2.6 on 2021-09-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_auto_20210916_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'city', 'verbose_name_plural': 'cities'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'country', 'verbose_name_plural': 'countries'},
        ),
        migrations.AlterModelOptions(
            name='description',
            options={'verbose_name': 'description', 'verbose_name_plural': 'descriptions'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'tag', 'verbose_name_plural': 'tags'},
        ),
        migrations.AddField(
            model_name='trip',
            name='short_description',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='short_description'),
        ),
    ]