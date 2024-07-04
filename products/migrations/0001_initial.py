# Generated by Django 4.2.13 on 2024-07-04 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('price', models.FloatField(default=0.0)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
    ]
