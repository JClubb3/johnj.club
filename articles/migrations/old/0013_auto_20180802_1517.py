# Generated by Django 2.0.7 on 2018-08-02 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20180802_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='series',
            options={'ordering': ['-latest_article_date'], 'verbose_name_plural': 'series'},
        ),
    ]