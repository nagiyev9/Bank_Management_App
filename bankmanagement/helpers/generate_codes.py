import random
from datetime import date
from dateutil.relativedelta import relativedelta

def generate_confirm_code():
    return random.randint(100000, 999999)

def generate_credit_card_number():
    first_4 = random.randint(1000, 9999)
    second_4 = random.randint(1000, 9999)
    return f'4155 7346 {first_4} {second_4}'

def generate_cvv():
    return random.randint(100, 999)

def generate_expire_date():
    return date.today() + relativedelta(years=3)