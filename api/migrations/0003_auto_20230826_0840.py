# Generated by Django 3.2.15 on 2023-08-26 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('api', '0002_ebtcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='target_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to='contenttypes.contenttype'),
        ),
    ]
