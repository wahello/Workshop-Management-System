# Generated by Django 2.0.7 on 2018-07-29 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0004_auto_20180729_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salarylist',
            old_name='recordiron',
            new_name='recordIron',
        ),
        migrations.RenameField(
            model_name='salarylist',
            old_name='recordsew',
            new_name='recordSew',
        ),
        migrations.RenameField(
            model_name='salarylist',
            old_name='recordtailor',
            new_name='recordTailor',
        ),
    ]