# Generated by Django 5.1.3 on 2024-12-31 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_customusermodel_is_verficated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nazwa użytkownika'),
        ),
    ]
