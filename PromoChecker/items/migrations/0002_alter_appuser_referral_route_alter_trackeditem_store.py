# Generated by Django 4.0.6 on 2023-01-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='referral_route',
            field=models.CharField(blank=True, choices=[('search', 'search'), ('other', 'other'), ('social', 'social'), ('friends', 'friends')], max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='trackeditem',
            name='store',
            field=models.CharField(blank=True, choices=[('asos', 'asos'), ('zalando', 'zalando')], max_length=12, null=True),
        ),
    ]
