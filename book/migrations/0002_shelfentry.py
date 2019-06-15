# Generated by Django 2.2.1 on 2019-06-15 17:16

import book.constants
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShelfEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('shelf', models.SmallIntegerField(choices=[(1, book.constants.Shelf(1)), (2, book.constants.Shelf(2)), (3, book.constants.Shelf(3))], db_index=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
