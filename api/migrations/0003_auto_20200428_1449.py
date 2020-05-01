# Generated by Django 3.0.5 on 2020-04-28 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200428_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='albums',
        ),
        migrations.AddField(
            model_name='picture',
            name='albums',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Album'),
        ),
    ]