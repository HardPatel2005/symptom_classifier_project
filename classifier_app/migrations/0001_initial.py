# Generated by Django 5.2.4 on 2025-07-14 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SymptomEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom_text', models.TextField()),
                ('classification', models.CharField(blank=True, max_length=50, null=True)),
                ('response_message', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Symptom Entries',
                'ordering': ['-timestamp'],
            },
        ),
    ]
