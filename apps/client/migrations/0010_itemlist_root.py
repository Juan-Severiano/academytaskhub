# Generated by Django 4.2.2 on 2023-07-03 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_alter_itemlist_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemlist',
            name='root',
            field=models.BooleanField(default=False),
        ),
    ]
