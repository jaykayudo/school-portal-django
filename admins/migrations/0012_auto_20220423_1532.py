# Generated by Django 2.2.2 on 2022-04-23 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0011_auto_20220422_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admins.Class'),
        ),
    ]
