# Generated by Django 3.1 on 2021-06-29 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210625_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title', 'price']},
        ),
    ]