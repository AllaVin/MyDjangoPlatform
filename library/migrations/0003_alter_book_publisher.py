# Generated by Django 5.2.1 on 2025-06-23 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_publisher_book_publisher_real"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="publisher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="library.member",
                verbose_name="Member",
            ),
        ),
    ]
