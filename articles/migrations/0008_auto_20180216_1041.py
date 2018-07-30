# Generated by Django 2.0 on 2018-02-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_author_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.TextField(default='', help_text="I mean. It's a bio."),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(help_text='A no space name to be used for URLs'),
        ),
        migrations.AlterField(
            model_name='series',
            name='slug',
            field=models.SlugField(help_text='The short version of the name to use in URLs'),
        ),
    ]