# Generated by Django 3.0.4 on 2020-03-22 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='url_title',
            field=models.CharField(default='speculaastaart', max_length=100),
        ),
    ]
