# Generated by Django 5.0.2 on 2024-03-27 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="subtype",
            field=models.CharField(
                choices=[
                    ("", "Empty"),
                    ("message_changed", "Message Changed"),
                    ("message_replied", "Message Replied"),
                    ("channel_joined", "Channel Joined"),
                    ("bot_message", "Bot Message"),
                ],
                db_index=True,
                default="",
                max_length=40,
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="type",
            field=models.CharField(choices=[("message", "Message")], db_index=True, default="message", max_length=40),
        ),
    ]
