# Generated by Django 4.2.4 on 2023-08-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_alter_traininginfo_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininginfo',
            name='weekdays',
            field=models.CharField(choices=[('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')], max_length=128),
        ),
    ]
