# Generated by Django 2.2.3 on 2020-02-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]