# Generated by Django 3.1.4 on 2020-12-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=55, null=True)),
                ('Number', models.CharField(max_length=15, null=True)),
                ('Income', models.FloatField(null=True)),
                ('Data', models.DateTimeField(null=True)),
                ('Visit_status', models.TextField(null=True)),
                ('Visit_count', models.IntegerField(null=True)),
            ],
        ),
    ]
