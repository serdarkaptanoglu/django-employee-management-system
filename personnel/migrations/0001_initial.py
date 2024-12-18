# Generated by Django 5.1.3 on 2024-12-02 22:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, verbose_name='Mail Adresi')),
                ('password', models.CharField(max_length=50, verbose_name='Şifre')),
                ('role', models.CharField(blank=True, max_length=25, null=True, verbose_name='Rol')),
                ('annual_leave_days', models.IntegerField(default=15, verbose_name='Yıllık İzin Hakkı')),
                ('remaining_leave_days', models.IntegerField(default=15, verbose_name='Kalan İzin Günleri')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif Mi?')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Güncellenme Tarihi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı Adı')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeWorkInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_work', models.DateTimeField(auto_now_add=True, verbose_name='İşe Başlama Saati')),
                ('ended_work', models.DateTimeField(blank=True, null=True, verbose_name='İşten Çıkış Saati')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif Mi?')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')),
                ('updated_date', models.DateTimeField(blank=True, null=True, verbose_name='Güncellenme Tarihi')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personnel.employee', verbose_name='Personel')),
            ],
        ),
    ]
