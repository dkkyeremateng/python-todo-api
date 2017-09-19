from keep.extensions import db
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from config import settings


class User(db.Document):
    """
    This is the user model
    """
    external_id = db.StringField(required=True)
    email = db.EmailField(required=True, min_length=1, unique=True)
    password = db.StringField(required=True, min_length=6)
    tokens = db.DictField()

    def generate_auth_token(self):
        payloads = {
            'id': self.external_id,
            'access': 'auth'
        }

        token = str(jwt.encode(payloads, settings.SECRET_KEY))[2:-1]

        self.tokens = {'access': payloads['access'], 'token': token}

        return self.save()

    def remove_auth_token(self, token):
        tokens = {
            'access': 'auth',
            'token': token
        }

        self.tokens = None

        return self.save()

    @classmethod
    def find_by_token(cls, token):

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY)

            tokens = {
                'access': 'auth',
                'token': token
            }

            return User.objects.filter(external_id=decoded.get('id'),
                                       tokens=tokens).first()
        except Exception:
            return None

    @classmethod
    def find_by_email(cls, email):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.objects.filter(email=email).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    def authenticated(self, with_password=True, password=''):
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            return check_password_hash(self.password, password)

        return True
