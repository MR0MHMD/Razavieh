from .forms import CustomUserRegisterForm, UserEditForm, OTPVerifyForm, MobileLoginForm
from django.contrib.auth.decorators import login_required
from .sms_utils import send_verification_code, generate_otp, send_otp_via_ghasedak
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from report.models import ReportLike
from django.contrib import messages
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta


def register(request):
    """
    ثبت‌نام کاربر:
    - اطلاعات فرم را در session نگه می‌دارد
    - OTP تولید و ارسال می‌کند
    - کاربر هنوز ساخته نشده است
    """
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # ذخیره داده‌ها در session
            request.session['register_data'] = form.cleaned_data

            # تولید OTP
            code = generate_otp()
            request.session['register_otp'] = code
            request.session['otp_created_at'] = timezone.now().isoformat()

            # ارسال OTP
            send_otp_via_ghasedak(form.cleaned_data['phone_number'], code)

            return redirect('accounts:otp-verify', phone_number=form.cleaned_data['phone_number'])
    else:
        form = CustomUserRegisterForm()
    return render(request, 'accounts/registration/register.html', {'form': form})


def otp_verify(request, phone_number):
    """
    تأیید OTP:
    - داده‌های فرم از session خوانده می‌شوند
    - در صورت صحت OTP، کاربر ساخته و وارد می‌شود
    """
    otp = request.session.get('register_otp')
    otp_time = request.session.get('otp_created_at')
    register_data = request.session.get('register_data')

    if not otp or not register_data:
        messages.error(request, "لطفاً ابتدا ثبت‌نام را انجام دهید.")
        return redirect('accounts:register')

    # بازیابی کاربر از دیتابیس (در صورت ورود بعد از OTP)
    try:
        user = CustomUser.objects.get(phone_number=phone_number)
        user_exists = True
    except CustomUser.DoesNotExist:
        user = None
        user_exists = False

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code_input = form.cleaned_data['code']

            # بررسی کد و محدودیت زمانی 2 دقیقه
            otp_created_at_dt = timezone.datetime.fromisoformat(otp_time)
            if code_input != otp:
                form.add_error('code', "کد اشتباه است.")
            elif timezone.now() > otp_created_at_dt + timedelta(minutes=2):
                form.add_error('code', "کد منقضی شده است.")
            else:
                # اگر کاربر هنوز ساخته نشده، ایجاد می‌کنیم
                if not user_exists:
                    user = CustomUser.objects.create_user(
                        username=register_data['username'],
                        phone_number=register_data['phone_number'],
                        password=register_data['password'],
                        first_name=register_data.get('first_name', ''),
                        last_name=register_data.get('last_name', ''),
                    )

                # ورود کاربر
                login(request, user)

                # پاک کردن داده‌های session
                request.session.pop('register_data', None)
                request.session.pop('register_otp', None)
                request.session.pop('otp_created_at', None)

                return redirect('accounts:profile')
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
