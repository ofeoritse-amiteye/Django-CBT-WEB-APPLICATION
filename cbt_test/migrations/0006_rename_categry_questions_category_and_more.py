# Generated by Django 4.2.4 on 2024-08-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbt_test', '0005_user_score_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='categry',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='user_score',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
