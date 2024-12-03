from datetime import time, datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Kullanıcı Adı')
    email = models.EmailField(max_length=100, verbose_name='Mail Adresi')
    password = models.CharField(max_length=50, verbose_name='Şifre')
    role = models.CharField(max_length=25, blank=True, null=True, verbose_name='Rol')
    annual_leave_days = models.IntegerField(default=15, verbose_name='Yıllık İzin Hakkı')
    remaining_leave_days = models.IntegerField(default=15, verbose_name='Kalan İzin Günleri')
    is_active = models.BooleanField(default=True, verbose_name='Aktif Mi?')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')
    updated_date = models.DateTimeField(blank=True, null=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return f'{self.user}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance, email=instance.email)


post_save.connect(create_profile, sender=User)


class EmployeeWorkInfo(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Personel')
    started_work = models.DateTimeField(auto_now_add=True, verbose_name='İşe Başlama Saati')
    ended_work = models.DateTimeField(null=True, blank=True, verbose_name='İşten Çıkış Saati')
    is_active = models.BooleanField(default=True, verbose_name='Aktif Mi?')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')
    updated_date = models.DateTimeField(blank=True, null=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return f'{self.employee.user}'

    def calculate_lateness(self):
        work_start_time = time(8, 0)
        actual_start_time = self.started_work.time()
        if actual_start_time > work_start_time:
            delay = datetime.combine(self.started_work.date(), actual_start_time) - \
                    datetime.combine(self.started_work.date(), work_start_time)
            return delay.total_seconds() / 60
        return 0


class LeaveRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Personel")
    start_date = models.DateField(verbose_name="İzin Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="İzin Bitiş Tarihi")
    reason = models.TextField(verbose_name="İzin Nedeni")
    leave_days = models.IntegerField(null=True, blank=True, verbose_name="Talep Edilen İzin Günleri")
    is_approved = models.BooleanField(null=True, blank=True, verbose_name="Onay Durumu")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Talep Tarihi")

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.leave_days = delta.days + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date}"
