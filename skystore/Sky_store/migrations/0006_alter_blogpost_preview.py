# Generated by Django 4.2.1 on 2023-05-30 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sky_store', '0005_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Картинка'),
        ),
    ]