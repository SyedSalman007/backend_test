# Generated by Django 5.0.7 on 2025-03-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orders_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='user',
        ),
        migrations.AddField(
            model_name='orders',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
            preserve_default=False,
        ),
    ]
