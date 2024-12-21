from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from twilio.rest import Client

from .models import User
from account.models import Account, Card
from .forms import SignupForm, LoginForm, ConfirmationCodeViaPhone, ConfirmationCodeViaEmail
from bankmanagement.helpers.generate_codes import generate_confirm_code, generate_credit_card_number, generate_cvv, generate_expire_date
from bankmanagement.helpers.messages.confirmation_code_messages import send_confirmation_code_email, send_confirmation_code_phone

# Create your views here.

# Signup
def signup(request):

    form = SignupForm(request.POST or None)

    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        gender = form.cleaned_data.get("gender")
        number = form.cleaned_data.get("number")
        birthday_date = form.cleaned_data.get("birthday_date")
        password = form.cleaned_data.get("password")

        birthday_date_str = birthday_date.strftime('%Y-%m-%d')

        existing_user = User.objects.filter(username=username) | User.objects.filter(email=email)

        if existing_user.exists():
            if existing_user.filter(email=email).exists():
                form.add_error('email', 'Email already registered')
            if existing_user.filter(username=username).exists():
                form.add_error('username', 'Username already taken')
            return render(request, 'auth/signup.html', {'form': form})

        try:
            validate_password(password, user=User)
        except ValidationError as errors:
            for error in errors:
                form.add_error('password', error)
            return render(request, 'auth/signup.html', {'form': form})


        request.session['signup_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'gender': gender,
            'number': number,
            'birthday_date': birthday_date_str,
            'password': password
        }

        
        confirm_code = generate_confirm_code()

        
        request.session['confirm_code'] = confirm_code

        return redirect("user:confirm-method")
    
    context = {
        'form': form
    }

    return render(request, 'auth/signup.html', context)

# Login
def login(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        usernameOrEmail = form.cleaned_data.get("usernameOrEmail")
        password = form.cleaned_data.get("password")

        user = User.objects.filter(username=usernameOrEmail).first() or User.objects.filter(email=usernameOrEmail).first()

        if user is None:
            messages.info(request, "Login failed. Please check fields and try again.")
            return redirect("user:login")
        
        checkPassword = user.check_password(password)

        if checkPassword:
            request.session['userID'] = str(user.id)
            return redirect("index")
        else:
            messages.info(request, "Login failed. Please check fields and try again.")
            return redirect("user:login")

    return render(request, 'auth/login.html', {'form': form})

# Choose Confirmation Method
def choose_confirm_method(request):

    if request.method == "POST":
        
        method = request.POST.get('method')

        if method == "email":

            first_name = request.session.get('signup_data').get('first_name')
            last_name = request.session.get('signup_data').get('last_name')
            email = request.session.get('signup_data').get('email')

            confirm_code = request.session.get('confirm_code')

            try:
                send_mail(
                    'Confirm Your Email',
                    send_confirmation_code_email(first_name, last_name, confirm_code),
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                messages.success(request, "Confirmation code sent to your email.")
                return redirect("user:confirm-via-email")

            except Exception as e:
                messages.error(request, f"Error sending confirmation email: {str(e)}")
        
        elif method == "phone":

            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            twilio_phone_number = settings.TWILIO_PHONE_NUMBER

            user_number = request.session.get('signup_data').get('number')

            confirmation_code = generate_confirm_code()
            request.session['confirm_code'] = confirmation_code

            client = Client(account_sid, auth_token)

            try:
                message = client.messages.create(
                    body=send_confirmation_code_phone(confirmation_code),
                    from_=twilio_phone_number,
                    to=user_number
                )

                request.session['message_sid'] = message.sid
                messages.success(request, "Confirmation code sent to your phone.")
                return redirect("user:confirm-via-phone")
            except Exception as e:
                messages.info(request, f"Error sending confirmation code: {str(e)}")

    return render(request, 'auth/confirm-choice.html')

# Confirm via Email
def confirm_via_email(request):

    signup_data = request.session.get('signup_data')
    confirm_code = request.session.get('confirm_code')

    if not signup_data or not confirm_code:
        messages.error(request, "Session data not found")
        return redirect("user:signup")
    
    form = ConfirmationCodeViaEmail(request.POST or None)

    if form.is_valid():
        code = form.cleaned_data.get("code")

        if not signup_data:
            return redirect("user:signup")
        
        if code != str(confirm_code):
            messages.info(request, "Invalid confirmation code")
            return redirect("user:confirm-via-email")

        first_name = signup_data['first_name']
        last_name = signup_data["last_name"]
        username = signup_data["username"]
        email = signup_data["email"]
        gender = signup_data["gender"]
        number = signup_data["number"]
        birthday_date = signup_data["birthday_date"]
        password = signup_data["password"]

        newUser = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            gender=gender,
            number=number,
            birthday_date=birthday_date
        )
        newUser.set_password(password)
        newUser.save()

        del request.session['confirm_code']
        del request.session['signup_data']

        get_new_user_id = str(User.objects.filter(first_name=str(newUser).split(' ')[0]).first().id)

        request.session['userID'] = get_new_user_id

        # Create new user card
        new_card = Card.objects.create(
            user=newUser,
            card_number=generate_credit_card_number(),
            card_cvv=generate_cvv(),
            card_expire_date=generate_expire_date()
        )

        # Crete new user account
        new_account = Account.objects.create(
            user=newUser,
            profile_url=f'http://127.0.0.1:8000/account/{get_new_user_id}',
            card=new_card
        )

        new_account.transaction_history.set([])

        messages.success(request, "Singup successfully compleated")
        return redirect("index")

    context = {
        'form': form
    }

    return render(request, 'auth/email-confirm.html', context)

# Confirm via Phone
def confirm_via_phone(request):

    signup_data = request.session.get('signup_data')
    confirm_code = request.session.get('confirm_code')


    if not signup_data or not confirm_code:
        messages.error(request, "Session data not found")
        return redirect("user:signup")

    form = ConfirmationCodeViaPhone(request.POST or None)

    if form.is_valid():
        code = form.cleaned_data.get("code")

        if code != str(confirm_code):
            messages.info(request, "Invalid confirmation code")
            return redirect("user:confirm-via-phone")

        first_name = signup_data["first_name"]
        last_name = signup_data["last_name"]
        username = signup_data["username"]
        email = signup_data["email"]
        gender = signup_data["gender"]
        number = signup_data["number"]
        birthday_date = signup_data["birthday_date"]
        password = signup_data["password"]

        newUser = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            gender=gender,
            number=number,
            birthday_date=birthday_date
        )
        newUser.set_password(password)
        newUser.save()

        del request.session['confirm_code']
        del request.session['signup_data']

        
        get_new_user_id = str(User.objects.filter(first_name=str(newUser).split(' ')[0]).first().id)

        request.session['userID'] = get_new_user_id

         # Create new user card
        new_card = Card.objects.create(
            user=newUser,
            card_number=generate_credit_card_number(),
            card_cvv=generate_cvv(),
            card_expire_date=generate_expire_date()
        )

        # Crete new user account
        new_account = Account.objects.create(
            user=newUser,
            profile_url=f'http://127.0.0.1:8000/account/{get_new_user_id}',
            card=new_card
        )

        new_account.transaction_history.set([])

        messages.success(request, "Singup successfully compleated")
        return redirect("index")

    return render(request, 'auth/number-confirm.html')

# Logout
def logout(request):

    if request.session.get('userID'):
        del request.session['userID']
    
    return redirect("user:login")