# Generated by Django 4.1.1 on 2022-09-19 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sensor',
            fields=[
                ('macAddress', models.CharField(max_length=19, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('interval', models.IntegerField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='datas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_stamp', models.BigIntegerField()),
                ('value', models.BigIntegerField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.sensor')),
            ],
            options={
                'ordering': ['t_stamp'],
            },
        ),
    ]