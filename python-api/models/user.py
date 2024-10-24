# models.py
from db_config import get_db
import bcrypt
import jwt
from datetime import datetime, timedelta

class User:
    def __init__(self, email, name, phone, billing_address=None, city=None, state=None, postal_code=None, country =None,password=None, user_image=None,):
        self.email = email
        self.name = name
        self.phone = phone
        self.user_image = user_image
        self.password = password
        self.email_confirmed = False
        self.confirmation_code = None
        self.reset_token = None
        self.reset_token_expiry = None
        self.mfa_enabled = False
        self.mfa_method = 'email'
        self.totp_secret = None
        self.billing_address = billing_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_auth_token(self, secret_key):
        token = jwt.encode(
            {'email': self.email, 'exp': datetime.utcnow() + timedelta(days=1)},
            secret_key,
            algorithm='HS256'
        )
        return token

    def save(self):
        db = get_db()
        user_data = self.__dict__.copy()
        db.users.insert_one(user_data)  # Save user data as a document

    @staticmethod
    def find_by_email(email):
        db = get_db()
        user_data = db.users.find_one({'email': email})
        return User(**user_data) if user_data else None

    def verify_reset_token(self, token):
        is_match = self.reset_token == token
        is_expired = self.reset_token_expiry and self.reset_token_expiry < datetime.utcnow()
        return is_match and not is_expired
