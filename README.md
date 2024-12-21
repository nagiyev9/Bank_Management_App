# Bank Management System

A secure and feature-rich Bank Management System built using Django, MySQL, and Jinja templates. This project supports user registration, email and phone number verification, secure fund transfers between users, deposits from external bank cards, and detailed account management.

---

## Features

### User Management
- Secure user registration and login.
- Custom user model for flexible account handling.
- Email and phone number verification using Twilio API and SMTP.

### Banking Operations
- Transfer funds between users securely.
- Deposit money from external bank cards.
- View account balances and transaction history.

### Security
- Uses Django's built-in CSRF protection and password validation.
- Sensitive information (e.g., secret keys, database credentials) managed using environment variables.

---

## Technologies Used

### Backend
- Django 5.1.4
- MySQL database
- Python 3.11+

### Frontend
- Jinja2 templates
- Crispy Forms with Bootstrap 5 integration

### APIs and Libraries
- Twilio API for phone number verification
- SMTP for email verification
- Django REST framework (optional for APIs)

---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.11+
- MySQL database
- pip (Python package manager)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/bank-management.git
   cd bank-management
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env` File**:
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=bank_management
   DB_USER=root
   DB_PASSWORD=your-db-password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   TWILIO_ACCOUNT_SID=your-twilio-account-sid
   TWILIO_AUTH_TOKEN=your-twilio-auth-token
   TWILIO_PHONE_NUMBER=your-twilio-phone-number
   ```

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Usage

1. **User Registration**:
   - Register using your email and phone number.
   - Verify your email and phone via OTP.

2. **Deposit Funds**:
   - Add money to your account from external bank cards.

3. **Transfer Funds**:
   - Securely transfer funds to other users within the system.

4. **View Transactions**:
   - View your transaction history and account details.

---

## License

This project is licensed under the MIT License.

---

## Author
**Mahaddin Nagiyev**

For questions or support, feel free to contact [meheddinngyv9@gmail.com](mailto:meheddinngyv9@gmail.com).

## Images

![image](https://github.com/user-attachments/assets/c91fe46f-d7b6-4675-8a0d-8949b937201c)

![image](https://github.com/user-attachments/assets/92420e6b-ae11-4b10-81fe-0a2be33e392a)

![image](https://github.com/user-attachments/assets/2a358a85-89a3-41ac-b415-d46afd4e2e34)

![image](https://github.com/user-attachments/assets/67d26bf4-6838-44cb-a755-91c04b3716df)

![image](https://github.com/user-attachments/assets/25d9e38c-8eb7-49d0-93c3-e8bd1ba896bc)

![Uploading image.png…]()



