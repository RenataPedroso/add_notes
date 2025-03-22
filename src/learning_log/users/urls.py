from django.urls import path
#importando uma view propria do django para login, que faz a verificacao de login e senha e autentica o user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]