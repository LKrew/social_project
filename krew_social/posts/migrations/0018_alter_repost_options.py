# Generated by Django 4.0.2 on 2022-09-01 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_rename_user_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repost',
            options={'ordering': ['-created_at']},
        ),
    ]