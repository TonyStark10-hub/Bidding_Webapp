# Generated by Django 3.0.8 on 2020-10-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201007_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('newbid', models.IntegerField()),
                ('title', models.CharField(max_length=64)),
                ('item_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('item_id', models.IntegerField()),
            ],
        ),
    ]
