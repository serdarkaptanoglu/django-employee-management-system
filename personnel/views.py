from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from .forms import EmployeeRegisterForm, LoginForm, UpdateUserForm, LeaveRequestForm
from .models import Employee, EmployeeWorkInfo, LeaveRequest
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def home(request):
    return render(request, 'home.html')


def login_home(request):
    return render(request, 'login_home.html')


def register(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kullanıcı başarıyla oluşturuldu!')
            return redirect('home')
    else:
        form = EmployeeRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_personnel(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Hoş geldiniz, {user.username}!')
            return redirect('personnel_dashboard')
    form = LoginForm()
    return render(request, 'login_personnel.html', {'form': form})


def login_manager(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                messages.success(request, f'Hoş geldiniz, {user.username}!')
                return redirect('manager_dashboard')
            messages.info(request, "Erişim reddedildi.")
    else:
        form = LoginForm()
    return render(request, 'login_manager.html', {'form': form})


@login_required(login_url="user:login")
def manager_dashboard(request):
    if request.user.is_superuser:
        employees = Employee.objects.all()
        return render(request, "manager_dashboard.html", {'employees': employees})
    else:
        messages.info(request, "Erişim reddedildi. Bu sayfaya yalnızca yetkililer erişebilir.")
        return redirect("home")


def person_info(request, id):
    if request.user.id == id:
        employee = Employee.objects.get(id=id)
        return render(request, 'personnel_info.html', {'employee': employee})
    else:
        messages.info(request, "Erişim reddedildi. Yalnızca kendi bilgilerinizi görebilirsiniz.")
        return redirect("home")


def logout_ems(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yaptınız..")
    return redirect("home")


@login_required(login_url="user:login")
def update_user(request, id):
    current_user = User.objects.get(id=id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    if user_form.is_valid():
        user_form.save()
        login(request, current_user)
        messages.success(request, "Kullanıcı güncellendi..")
        return redirect('update_user', id=current_user.id)
    return render(request, 'update_user.html', {'user_form': user_form})


def personnel_dashboard(request):
    employee = User.objects.all()
    return render(request, 'personnel_dashboard.html', {'employee': employee})


def late_employees_view(request):
    if not request.user.is_superuser:
        messages.info(request, "Bu sayfaya yalnızca yöneticiler erişebilir.")
        return redirect('home')

    today = localtime().date()
    late_employees = []

    work_infos = EmployeeWorkInfo.objects.filter(started_work__date=today)
    for work_info in work_infos:
        lateness_minutes = work_info.calculate_lateness()
        if lateness_minutes > 0:
            late_employees.append({
                'employee': work_info.employee,
                'lateness_minutes': round(lateness_minutes, 2),
                'started_work': localtime(work_info.started_work),
            })

    context = {
        'late_employees': late_employees
    }
    return render(request, 'late_employees.html', context)


@login_required
def request_leave(request):
    employee = request.user.employee
    if employee.remaining_leave_days <= 0:
        messages.info(request, "Yıllık izniniz bulunmamaktadır. Yeni bir izin talebi oluşturamazsınız.")
        return redirect('personnel_dashboard')
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, employee=employee)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, 'İzin talebiniz başarıyla oluşturuldu.')
            return redirect('personnel_dashboard')
    else:
        form = LeaveRequestForm(employee=employee)

    return render(request, 'request_leave.html', {
        'form': form,
        'remaining_days': employee.remaining_leave_days
    })


@login_required
def manage_leave_requests(request):
    if not request.user.is_superuser:
        messages.info(request, "Bu sayfaya yalnızca yöneticiler erişebilir.")
        return redirect('home')

    leave_requests = LeaveRequest.objects.all()
    return render(request, 'manage_leave_requests.html', {'leave_requests': leave_requests})


@login_required
def approve_leave(request, leave_id):
    if not request.user.is_superuser:
        messages.info(request, "Bu işlem yalnızca yöneticilere açıktır.")
        return redirect('home')

    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    leave_request.is_approved = True
    leave_request.save()
    messages.success(request, "İzin talebi onaylandı.")
    return redirect('manage_leave_requests')


@login_required
def reject_leave(request, leave_id):
    if not request.user.is_superuser:
        messages.info(request, "Bu işlem yalnızca yöneticilere açıktır.")
        return redirect('home')

    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    leave_request.is_approved = False
    leave_request.save()
    messages.warning(request, "İzin talebi reddedildi.")
    return redirect('manage_leave_requests')
