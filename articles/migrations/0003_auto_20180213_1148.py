# Generated by Django 2.0 on 2018-02-13 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20180213_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='series',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='articles.Series'),
        ),
    ]
