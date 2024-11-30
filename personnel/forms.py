from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from personnel.models import LeaveRequest


class EmployeeRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail Adresiniz'}),
        label='Email Adresi'
    )
    password1 = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifrenizi Girin'}),
        required=True
    )
    password2 = forms.CharField(
        label='Şifreyi Onayla',
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifrenizi Tekrar Girin'}),
        required=True
    )
    is_staff = forms.BooleanField(required=True, initial=True, label="Staff Yetkisi")
    is_superuser = forms.BooleanField(required=False, initial=False, label="Superuser Yetkisi")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-mail adresiyle bir kullanıcı zaten mevcut.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Şifreler eşleşmiyor!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Kullanıcı Adı veya E-mail'}),
        label='Kullanıcı Adı veya E-mail'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifre'}),
        label='Şifre'
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username_or_email, password=password)

        if not user:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if not user:
            raise ValidationError("Kullanıcı adı, e-posta veya şifre yanlış!")

        self.confirm_login_allowed(user)
        return cleaned_data


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'annual_leave_days', 'remaining_leave_days')

    password = None
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
                             required=False)
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                 required=False)
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                required=False)
    annual_leave_days = forms.CharField(label="", max_length=100, initial=15,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'Annual Leave Days'}),
                                        required=False)
    remaining_leave_days = forms.CharField(label="", max_length=100, initial=15,
                                           widget=forms.TextInput(
                                               attrs={'class': 'form-control', 'placeholder': 'Remaining Leave Days'}),
                                           required=False)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            delta = (end_date - start_date).days + 1

            if self.employee and self.employee.remaining_leave_days <= 0:
                raise forms.ValidationError(
                    "Yıllık izniniz bulunmamaktadır. Yeni bir izin talep edemezsiniz."
                )
            elif self.employee and self.employee.remaining_leave_days < delta:
                raise forms.ValidationError(
                    f"Talep ettiğiniz gün sayısı ({delta} gün), kalan izin günlerinizden fazla. "
                    f"Kalan izin günleriniz: {self.employee.remaining_leave_days} gün."
                )
        return cleaned_data
