# Generated by Django 3.2.9 on 2021-11-24 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='temperament',
        ),
    ]
