# Generated by Django 5.0.6 on 2024-07-02 14:27

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='texto',
            field=django_quill.fields.QuillField(),
        ),
    ]
