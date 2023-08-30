# Generated by Django 4.1.3 on 2023-08-27 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, choices=[('proteins', 'Proteins'), ('creatines', 'Creatines'), ('vitamins', 'Vitamins'), ('amino-acids', 'Amino Acids'), ('pre-workout', 'Pre-Workout')], max_length=255, null=True)),
            ],
        ),
    ]