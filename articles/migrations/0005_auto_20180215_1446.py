# Generated by Django 2.0 on 2018-02-15 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20180214_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='series',
            options={},
        ),
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.TextField(help_text="I mean. It's a bio.", null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='description',
            field=models.TextField(default='', help_text='A description of the series'),
        ),
    ]
