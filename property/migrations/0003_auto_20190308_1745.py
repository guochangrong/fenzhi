# Generated by Django 2.1.3 on 2019-03-08 09:45

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_vicinity'),
    ]

    operations = [
        migrations.AddField(
            model_name='vicinity',
            name='vicinityData',
            field=djongo.models.fields.DictField(default={}, verbose_name='vicinityData'),
        ),
        migrations.AlterField(
            model_name='vicinity',
            name='projectName',
            field=models.CharField(default='', max_length=255, verbose_name='projectName'),
        ),
    ]
