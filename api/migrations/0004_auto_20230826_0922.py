# Generated by Django 3.2.15 on 2023-08-26 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20230826_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='target_id',
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.creditcard'),
        ),
    ]