# Generated by Django 3.1.1 on 2020-10-11 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201011_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.course'),
        ),
    ]