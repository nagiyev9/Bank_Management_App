from django.contrib import admin
from django.urls import path
from .views import signup, login, choose_confirm_method, confirm_via_email, confirm_via_phone, logout

app_name = "user"

urlpatterns = [
    path('login', login, name="login"),
    path('signup', signup, name = "signup"),
    path('signup/confirm-method', choose_confirm_method, name = "confirm-method"),
    path('signup/confirm-method/email', confirm_via_email, name = "confirm-via-email"),
    path('signup/confirm-method/phone', confirm_via_phone, name = "confirm-via-phone"),
    path('logout', logout, name = "logout"),
]