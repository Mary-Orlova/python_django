# Generated by Django 4.2 on 2023-08-11 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['pub_date'], 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
    ]
