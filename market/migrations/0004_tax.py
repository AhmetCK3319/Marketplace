# Generated by Django 5.0.1 on 2024-02-19 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_rename_date_added_cart_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_type', models.CharField(max_length=20, unique=True)),
                ('tax_percentage', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage (%)')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
