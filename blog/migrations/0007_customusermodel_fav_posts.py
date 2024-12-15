# Generated by Django 5.1.3 on 2024-12-14 22:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_customusermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='fav_posts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.postmodel', verbose_name='Ulubione posty'),
        ),
    ]
