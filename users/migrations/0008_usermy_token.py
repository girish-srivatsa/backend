# Generated by Django 3.1.1 on 2020-10-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20201011_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermy',
            name='token',
            field=models.TextField(default='owARGAhAHEreLJPJuj8UJuqXYVQbQxNwugjhl0wL'),
        ),
    ]