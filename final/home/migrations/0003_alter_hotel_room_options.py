# Generated by Django 4.2.5 on 2023-10-23 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_alter_hotel_room_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="hotel_room",
            options={"ordering": ["room_no"]},
        ),
    ]
