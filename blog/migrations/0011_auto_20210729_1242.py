# Generated by Django 3.2.5 on 2021-07-29 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_rename_images_postimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='album',
        ),
        migrations.DeleteModel(
            name='PostImage',
        ),
    ]
