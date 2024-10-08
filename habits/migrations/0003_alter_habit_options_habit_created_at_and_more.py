# Generated by Django 4.2 on 2024-08-31 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_alter_habit_periodicity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='habit',
            options={'verbose_name': 'привычка', 'verbose_name_plural': 'привычки'},
        ),
        migrations.AddField(
            model_name='habit',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='time_to_complete',
            field=models.DurationField(verbose_name='время на выполнение'),
        ),
    ]
