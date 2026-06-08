from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('',views.home,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path(
    'password-reset/',
    views.password_reset_request,
    name='password_reset'
),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
    'profile/',
    views.profile_view,
    name='profile'
),
path(
    'edit-profile/',
    views.edit_profile,
    name='edit_profile'
),

]
