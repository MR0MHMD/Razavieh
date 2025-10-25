from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect

from report.models import Report, ReportLike
from .froms import CustomUserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser


def register(request):
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'accounts/registration/register_done.html', {'user': user})
    else:
        form = CustomUserRegisterForm()
    return render(request, 'accounts/registration/register.html', {'form': form})


def log_out(request):
    logout(request)
    return render(request, 'accounts/registration/logged_out.html')


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
