from django.contrib import admin
from django.urls import path
from .views import profile_page, activate_card, deposit_set_price, deposit_card_details, search_user, send_money_to_user, send_money_to_bank_card

app_name = "account"

urlpatterns = [
    path('my-profile', profile_page, name="profile_page"),
    path('activate-card', activate_card, name="activate_card"),
    path('deposit/set-price', deposit_set_price, name="deposit_set_price"),
    path('deposit/card-details', deposit_card_details, name="deposit_card_details"),
    path('search', search_user, name="search_user"),
    path('send-money/to/<uuid:user_id>', send_money_to_user, name="send_money_to_user"),
    path('send-money/to/card', send_money_to_bank_card, name='send_money_to_bank_card'),
]