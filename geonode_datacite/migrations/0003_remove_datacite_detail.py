# Generated by Django 4.2.9 on 2024-11-20 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("geonode_datacite", "0002_alter_datacite_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datacite",
            name="detail",
        ),
    ]
