# Generated by Django 2.0.7 on 2018-08-08 18:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, help_text='Slugs are short versions of the title used for URLs', null=True)),
                ('content', models.TextField(help_text='Unlimited length. HTML formatted.')),
                ('shortline', models.CharField(help_text='A short summary to show in the sidebar and under the article title', max_length=200)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image_raw', models.ImageField(blank=True, null=True, upload_to='uploads/images')),
                ('image_thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/images')),
                ('image_thumbnail_transparent', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/images')),
                ('image_full', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/images')),
                ('audio', models.FileField(blank=True, null=True, upload_to='uploads/audio')),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-publish_date', '-date_modified'],
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('bio', models.TextField(help_text="I mean. It's a bio.")),
                ('image_raw', models.ImageField(blank=True, upload_to='uploads/')),
                ('image_thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/')),
                ('image_thumbnail_transparent', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/')),
                ('image_full', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/')),
                ('slug', models.SlugField(blank=True, editable=False, help_text='A no space name to be used for URLs', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The series this article should be filed under; will be used for URLs', max_length=40, unique=True)),
                ('description', models.TextField(default='', help_text='A description of the series')),
                ('slug', models.SlugField(blank=True, editable=False, help_text='The short version of the name to use in URLs', null=True)),
                ('image_raw', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('image_thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/')),
                ('image_thumbnail_transparent', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/')),
                ('image_full', models.ImageField(blank=True, editable=False, null=True, upload_to='uploads/')),
                ('latest_article_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'series',
                'ordering': ['-latest_article_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Tags used to help search for articles', max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='articles.Author'),
        ),
        migrations.AddField(
            model_name='article',
            name='series',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='articles.Series'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='articles.Tag'),
        ),
    ]