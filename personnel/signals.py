from datetime import datetime, time
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import EmployeeWorkInfo


@receiver(user_logged_in)
def log_work_start(sender, request, user, **kwargs):
    if not hasattr(user, 'employee'):
        return  # Eğer kullanıcı bir çalışan değilse, işlem yapılmaz.

    employee = user.employee
    today = datetime.now().date()
    work_info = EmployeeWorkInfo.objects.filter(employee=employee, started_work__date=today).first()

    if not work_info:
        now = datetime.now()
        work_info = EmployeeWorkInfo.objects.create(employee=employee, started_work=now)
        work_start_time = time(8, 0)  # 08:00
        if now.time() > work_start_time:
            delay_minutes = (datetime.combine(today, now.time()) - datetime.combine(today, work_start_time)).seconds // 60
            print(f"Kullanıcı {delay_minutes} dakika geç kaldı.")
        else:
            print("Kullanıcı zamanında işe başladı.")


def log_employee_work(sender, user, request, **kwargs):
    if user.is_authenticated and not user.is_superuser:
        EmployeeWorkInfo.objects.create(
            employee=user.employee,
            started_work=now()
        )