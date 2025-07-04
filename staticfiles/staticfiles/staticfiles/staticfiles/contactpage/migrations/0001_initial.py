# Generated by Django 5.2.1 on 2025-06-13 05:47

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.FileField(blank=True, default=None, max_length=250, null=True, upload_to='banners')),
                ('contact_des', models.CharField(blank=True, max_length=100, null=True)),
                ('second_heading', models.CharField(blank=True, max_length=100, null=True)),
                ('call_us_name', models.CharField(blank=True, max_length=100, null=True)),
                ('telphone_number_1', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_number_2', models.CharField(blank=True, max_length=100, null=True)),
                ('Email_us_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('email_2', models.CharField(blank=True, max_length=100, null=True)),
                ('Visit_us_name', models.CharField(blank=True, max_length=100, null=True)),
                ('location_address_name', models.CharField(blank=True, max_length=100, null=True)),
                ('office_opendays', models.CharField(blank=True, max_length=100, null=True)),
                ('office_time', models.CharField(blank=True, max_length=100, null=True)),
                ('short_heading_office', models.CharField(blank=True, max_length=100, null=True)),
                ('short_description', models.CharField(blank=True, max_length=100, null=True)),
                ('FAQ', tinymce.models.HTMLField(blank=True, null=True)),
            ],
        ),
    ]
