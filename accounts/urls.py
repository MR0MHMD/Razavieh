from django.contrib.auth import views as auth_views
from .froms import PersianSetPasswordForm
from django.urls import path, reverse_lazy
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/registration/login.html'), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/registration/password_reset_form.html',
            email_template_name='accounts/registration/password_reset_email.html',
            success_url='/accounts/password_reset/done/',
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password_reset_complete/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/registration/password_reset_confirm.html',
            form_class=PersianSetPasswordForm,
            success_url='/accounts/password_reset/complete/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile')
]



