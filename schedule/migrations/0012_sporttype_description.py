# Generated by Django 4.2.4 on 2023-08-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_alter_sporttype_managers_sporttype_slug_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sporttype',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]