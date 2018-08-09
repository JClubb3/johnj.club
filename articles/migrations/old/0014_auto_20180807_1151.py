# Generated by Django 2.0.7 on 2018-08-07 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20180802_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelWithImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_raw', models.ImageField(blank=True, upload_to='uploads/')),
                ('image_thumbnail', models.ImageField(blank=True, upload_to='uploads/')),
                ('image_full', models.ImageField(blank=True, upload_to='uploads/')),
            ],
        ),
        migrations.RemoveField(
            model_name='author',
            name='id',
        ),
        migrations.AddField(
            model_name='author',
            name='modelwithimages_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='articles.ModelWithImages'),
            preserve_default=False,
        ),
    ]