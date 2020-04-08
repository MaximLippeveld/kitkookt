# Generated by Django 3.0.4 on 2020-03-25 22:00

import ckeditor.fields
import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0016_recipe_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='date_published',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='intro',
            field=ckeditor.fields.RichTextField(),
        ),
    ]