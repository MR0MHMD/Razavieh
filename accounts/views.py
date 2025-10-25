from django.contrib.auth import logout
from django.shortcuts import render
from .froms import CustomUserRegisterForm


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
