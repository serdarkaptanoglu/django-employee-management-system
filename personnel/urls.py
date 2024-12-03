from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login-home/', views.login_home, name='login_home'),
    path('register/', views.register, name='register'),
    path('login-manager/', views.login_manager, name='login_manager'),
    path('login-personnel/', views.login_personnel, name='login_personnel'),
    path('logout/', views.logout_ems, name='logout'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('personnel-dashboard/', views.personnel_dashboard, name='personnel_dashboard'),
    path('person-info/<int:id>/', views.person_info, name='personnel_info'),
    path('update-user/<int:id>/', views.update_user, name='update_user'),
    path('late-employees/', views.late_employees_view, name='late_employees_view'),
    path('request-leave/', views.request_leave, name='request_leave'),
    path('manage-leave-requests/', views.manage_leave_requests, name='manage_leave_requests'),
    path('approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
]
