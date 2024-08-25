# Generated by Django 5.1 on 2024-08-25 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('alive', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='TestUser',
        ),
    ]
