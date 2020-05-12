from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.homepage, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='dashboard/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='dashboard/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='dashboard/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='dashboard/password_reset_complete.html'), name='password_reset_complete'),
    path('waf/auth_key_collect/', views.collect_auth_key, name='auth_key_collect'),
    path('waf/home/', views.waf_home, name='waf_home'),
    path('waf/detail/<zone_name>/', views.zone_details, name='waf-detail'),
    path('graph/try/', views.graph_try, name='graph')
]
