# Generated by Django 5.1.3 on 2024-12-02 23:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='İzin Başlangıç Tarihi')),
                ('end_date', models.DateField(verbose_name='İzin Bitiş Tarihi')),
                ('reason', models.TextField(verbose_name='İzin Nedeni')),
                ('leave_days', models.IntegerField(blank=True, null=True, verbose_name='Talep Edilen İzin Günleri')),
                ('is_approved', models.BooleanField(blank=True, null=True, verbose_name='Onay Durumu')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Talep Tarihi')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Personel')),
            ],
        ),
    ]
