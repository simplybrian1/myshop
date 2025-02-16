# Generated by Django 5.1.5 on 2025-02-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_rename_full_name_address_address_line_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line',
            new_name='street_address',
        ),
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(default='Unnamed User', max_length=255),
        ),
    ]
