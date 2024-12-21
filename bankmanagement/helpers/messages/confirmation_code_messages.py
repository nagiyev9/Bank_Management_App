def send_confirmation_code_email(first_name, last_name, confirmation_code):
    return f"""
    Hello {first_name} {last_name},

    Thank you for registering with us! To complete your registration process, please use the following confirmation code:

    Confirmation Code: {confirmation_code}

    Please enter this code on the confirmation page to verify your email address and finish signing up. If you didn't request this code, you can ignore this email.

    If you have any questions or need assistance, feel free to contact our support team.

    Best regards,
    The [Your App Name] Team
    """

def send_confirmation_code_phone(confirmation_code):
    return f"""
    Hello,

    Thank you for registering with us! To complete your registration process, please use the following confirmation code:

    Confirmation Code: {confirmation_code}

    Please enter this code on the confirmation page to verify your phone number and finish signing up. If you didn't request this code, you can ignore this message.

    If you have any questions or need assistance, feel free to contact our support team.

    Best regards,
    The Bank Management Team
    """
