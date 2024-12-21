from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from datetime import datetime

from user.models import User
from account.models import Account, Card, Transaction
from .forms import CardPasswordForm, SetDepositAmount, SetDepostCard, SearchUserForm, SendMoneyForm, TransferMoneyToBankCardForm

def check_logged_in(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('userID'):
            return func(request, *args, **kwargs)
        else:
            return redirect('user:login')
    return wrapper

# Home Page
def index(request):
    user_id = request.session.get('userID')

    if user_id:
        user = User.objects.filter(id=user_id).first()

        if not user:
            messages.info(request, "User not found.")
            return redirect('user:login')

        account = Account.objects.filter(user_id=user_id).first()
        transaction_history = Transaction.objects.filter(sender_user=user).first() or Transaction.objects.filter(reciever_user=user).first()

        context = {
            'account': account,
            'transaction_history': transaction_history
        }

        return render(request, 'index.html', context)
    return render(request, 'index.html')

# Profile Page
@check_logged_in
def profile_page(request):

    user_id = request.session.get('userID')

    if not user_id:
        messages.info(request, "You must be logged in to view this page.")
        return redirect('user:login')
    
    user = User.objects.filter(id=user_id).first()
    account = Account.objects.filter(user=user).first()

    today = datetime.now().date()

    transaction_history = (
        Transaction.objects.filter(sender_user=user, created_at__gte=today) |
        Transaction.objects.filter(reciever_user=user, created_at__gte=today)
    ).order_by('-created_at')

    if not user:
        messages.info(request, "User not found.")
        return redirect('user:login')
    
    context = {
        'user': user,
        'account': account,
        'transaction_history': transaction_history
    }
    
    return render(request, 'account/my-profile.html', context)

# Activate Card
@check_logged_in
def activate_card(request):
    
    user_id = request.session.get('userID')


    account = Account.objects.filter(user=user_id).first()

    if not account:
        messages.info(request, 'Account not found')
        return redirect('user:login')
    
    if account.card.is_active == True:
        messages.warning(request, 'Your card already activated')
        return redirect('account:profile_page')
    
    form = CardPasswordForm(request.POST or None)

    if form.is_valid():
        try:
            password = form.cleaned_data.get('password')
            card = Card.objects.filter(user=user_id).first()

            if not card:
                messages.info(request, 'Card not found')
                return redirect('user:login')
            
            card.card_password = make_password(password)
            card.is_active = True
            card.save()

            messages.success(request, 'Card has been activated')
            return redirect('account:profile_page')
            
        except ValidationError as error:
            form.add_error('password', error)
            return redirect('account:activate_card')

    context = {
        'form': form,
        'account': account
    }

    return render(request, 'account/card-activate.html', context)

# Set Deposit Price
@check_logged_in
def deposit_set_price(request):

    form = SetDepositAmount(request.POST or None)

    if form.is_valid():
        try:
            amount = form.cleaned_data.get('amount')

            request.session['deposit_amount'] = amount

            return redirect("account:deposit_card_details")
            
        except:
            if ValidationError:
                form.add_error('amount', ValidationError)

            messages.info(request, "Something went wrong")
            return redirect("account:deposit_set_price")
        
    context = {
        'form': form
    }

    return render(request, 'account/payment/deposit-price.html', context)

# Deposit Card Details
@check_logged_in
def deposit_card_details(request):
    form = SetDepostCard(request.POST or None)


    if form.is_valid():
        try:
            user_id = request.session.get('userID')

            if not user_id:
                messages.error(request, "User is not logged in.")
                return redirect("login")

            user_card = Card.objects.filter(user=user_id).first()
            amount = request.session.get('deposit_amount')

            if not amount:
                messages.error(request, "Deposit amount is not set in session.")
                return redirect("account:profile_page")
            print('view',form.cleaned_data.get('expiry_date'))

            card_number = form.cleaned_data.get('card_number')
            sender_name = form.cleaned_data.get('name_on_card')

            if not user_card:
                messages.info(request, "Card not found.")
                return redirect("account:profile_page")
            elif user_card.is_active == False:
                messages.info(request, "Your card has not been activated. Please activate your card first.")
                return redirect("account:profile_page")
            elif user_card.card_number == card_number:
                messages.info(request, "You cannot deposit to your own card.")
                return redirect("account:deposit_card_details")
            
            user_card.balance += int(amount)
            user_card.save()

            new_transaction = Transaction.objects.create(
                amount=amount,
                sender_name=sender_name,
                sender_card=card_number,
                reciever_user=user_card.user,
                balance_after_transaction=user_card.balance,
                transaction_type='deposit'
            )

            if not new_transaction:
                messages.error(request, "Transaction failed to save.")
                return redirect("account:deposit_card_details")
            
            new_transaction.save()
            del request.session['deposit_amount']

            messages.success(request, "Amount has been deposited successfully.")
            return redirect("account:profile_page")

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            if ValidationError:
                form.add_error('expirey_date_month', ValidationError)
            form.add_error(None, str(e))
            return redirect("account:deposit_card_details")

    deposit_amount = request.session.get('deposit_amount')

    context = {
        'form': form,
        'deposit_amount': deposit_amount
    }

    return render(request, 'account/payment/deposit-card-details.html', context)

# Search User
@check_logged_in
def search_user(request):
    query = request.GET.get('q', '')
    form = SearchUserForm(request.POST or None)

    users = None
    user_id = request.session.get('userID')

    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=user_id).order_by('username')

    context = {
        'form': form,
        'users': users,
        'query': query,
    }

    return render(request, 'account/search-user.html', context)

# Send Money To User
@check_logged_in
def send_money_to_user(request, user_id):

    form = SendMoneyForm(request.POST or None)
    sender_id = request.session.get('userID')

    if not sender_id:
        messages.info(request, "User is not logged in.")
        return redirect("login")

    if user_id == sender_id:
        messages.info(request, "You cannot send money to yourself.")
        return redirect("account:profile_page")
    
    sender = Card.objects.filter(user=sender_id).first()
    reciever = Card.objects.filter(user=user_id).first()

    if not sender:
        messages.info(request, "Sender card not found.")
        return redirect("account:search_user")
    elif not reciever:
        messages.info(request, "Reciever card not found.")
        return redirect("account:search_user")
    elif sender.is_active == False:
        messages.info(request, "Your card has not been activated. Please activate your card first.")
        return redirect("account:profile_page")
    elif reciever.is_active == False:
        messages.info(request, "Reciever card has not been activated")
        return redirect("account:search_user")
    elif sender.card_number == reciever.card_number:
        messages.info(request, "You cannot send money to your own card.")
        return redirect("account:search_user")

    if form.is_valid():
        try:
            amount = form.cleaned_data.get('amount')

            if sender.balance < int(amount):
                messages.info(request, "You don't have enough balance to send this amount.")
                return redirect("account:send_money_to_user", user_id=user_id)

            sender.balance -= int(amount)
            sender.save()

            reciever.balance += int(amount)
            reciever.save()

            new_transaction = Transaction.objects.create(
                amount=amount,
                sender_user=sender.user,
                sender_card=sender.card_number,
                reciever_user=reciever.user,
                balance_after_transaction=reciever.balance,
                transaction_type='money transfer',
            )

            if not new_transaction:
                messages.info(request, "Transaction failed to save.")
                return redirect("account:profile_page")

            new_transaction.save()

            messages.success(request, "Amount has been sent successfully.")
            return redirect("account:profile_page")

        except Exception as e:
            messages.info(request, f"Something went wrong: {str(e)}")
            if ValidationError:
                form.add_error('amount', ValidationError)
            form.add_error(None, str(e))            
            return redirect(
                "account:send_money_to_user",
                user_id=user_id
            )
        
    context = {
        'form': form,
        'reciever': reciever
    }

    return render(request, 'account/payment/send-money.html', context)

# Transfer Money To Bank Card
@check_logged_in
def send_money_to_bank_card(request):

    form = TransferMoneyToBankCardForm(request.POST or None)

    user_id = request.session.get('userID')

    sender = Card.objects.filter(user=user_id).first()

    if not user_id or not sender:
        return redirect('index')

    if form.is_valid():
        try:
            amount = form.cleaned_data.get('amount')
            card_number = form.cleaned_data.get('card_number')

            if sender.is_active != True:
                messages.info(request, "Your card has not been activated. Please activate your card first.")
                return redirect("account:profile_page")
            
            if sender.balance < int(amount):
                messages.info(request, "You don't have enough balance to send this amount.")
                return redirect("account:send_money_to_bank_card")
            
            elif card_number == sender.card_number:
                messages.info(request, "You cannot send money to your own card.")
                return redirect("account:search_user")
            
            sender.balance -= int(amount)
            sender.save()

            new_transaction = Transaction.objects.create(
                amount=amount,
                sender_user=sender.user,
                sender_card=sender.card_number,
                reciever_card=card_number,
                balance_after_transaction=sender.balance,
                transaction_type='money transfer',
            )

            new_transaction.save()

            if not new_transaction:
                messages.info(request, "Transaction failed to save.")
                return redirect("account:profile_page")

            messages.success(request, "Amount has been sent successfully.")
            return redirect('account:profile_page')
        except Exception as e:
            messages.info(request, f"Something went wrong: {str(e)}")
            if ValidationError:
                form.add_error('amount', ValidationError)
            form.add_error(None, str(e))
            return redirect("account:send_money_to_bank_card")
        
    context = {
        'form': form,
        'sender': sender
    }

    return render(request, 'account/payment/send-to-bank-card.html', context)
