from .forms import CustomUserRegisterForm, UserEditForm, OTPVerifyForm, MobileLoginForm
from django.contrib.auth.decorators import login_required
from .sms_utils import send_verification_code, verify_otp
from django.shortcuts import render, redirect
from django.contrib.auth import logout,login
from report.models import ReportLike
from django.contrib import messages
from .models import CustomUser


def register(request):
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()

            send_verification_code(user)

            return redirect('accounts:otp-verify', phone_number=user.phone_number)
    else:
        form = CustomUserRegisterForm()
    return render(request, 'accounts/registration/register.html', {'form': form})


def otp_verify(request, phone_number):
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
    except CustomUser.DoesNotExist:
        return redirect('accounts:register')

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            valid, message = verify_otp(user, code)
            if valid:
                login(request, user)
                return redirect('accounts:profile')
            else:
                form.add_error('code', message)
    else:
        form = OTPVerifyForm(initial={'phone_number': phone_number})

    return render(request, 'accounts/registration/otp_verify.html', {'form': form})


def log_out(request):
    logout(request)
    return render(request, 'accounts/registration/logged_out.html')


def mobile_login_request(request):
    if request.method == "POST":
        form = MobileLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                form.add_error('phone_number', "شماره موبایل در سیستم وجود ندارد.")
            else:
                send_verification_code(user)
                messages.success(request, "کد تأیید برای شما ارسال شد.")
                return redirect('accounts:otp-verify', phone_number=phone_number)
    else:
        form = MobileLoginForm()

    return render(request, 'accounts/registration/mobile_login.html', {'form': form})


@login_required(login_url='accounts:login')
def profile(request):
    user = request.user
    liked_reports = ReportLike.objects.filter(user=user).select_related('report')
    context = {'user': user, 'liked_reports': liked_reports}
    return render(request, 'accounts/registration/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'remove_photo' in request.POST:
                user.photo.delete(save=False)
                user.photo = None
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'accounts/registration/edit_profile.html', {'form': form})
