# Generated by Django 5.1.4 on 2024-12-11 22:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MemberAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assembly_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.assemblymember')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpeechRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('speech_order', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assembly_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.assemblymember')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.conference')),
            ],
            options={
                'ordering': ['conference', 'speech_order'],
            },
        ),
    ]
