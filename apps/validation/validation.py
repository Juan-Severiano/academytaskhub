from django.contrib import messages
from django.contrib.auth.models import User
import re


def username_is_valid(request: any, username: str) -> bool:
    if len(username) <= 0:
        messages.error(request, 'Prencha todos os campos.')
        return False
    return True

def email_is_valid(request: any, email: str, verify_exist: bool = True) -> bool:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@aluno\.ce\.gov\.br$'

    if len(email) <= 0:
        messages.error(request, 'Prencha todos os campos.')
        return False
    
    if verify_exist:
        email_exist = User.objects.filter(email=email).exists()
        if email_exist:
            messages.error(request, 'Email já utilizado')
            return False
    
    if not re.match(email_pattern, email):
        messages.error(request, 'O email precisa ser do gov.br')
        return False
    return True
    
def password_is_valid(request: any, password: str, confirm_password: str = '', verify_passwords: bool = True) -> bool:
    if len(password) <= 0:
        messages.error(request, 'Prencha todos os campos.')
        return False
    
    if verify_passwords:
        if len(confirm_password) <= 0:
            messages.error(request, 'Prencha todos os campos.')
            return False

        if password != confirm_password:
            messages.error(request, 'As senhas não coicidem')
            return False
    
    return True

def register_is_valid(request: any, username: str, email: str, password: str, confirm_password: str) -> bool:
    if not username_is_valid(request, username): return False
    if not email_is_valid(request, email): return False
    if not password_is_valid(request, password, confirm_password): return False
    return True

def login_is_valid(request: any, email: str, password: str) -> bool:
    if not email_is_valid(request, email, verify_exist=False): return False
    if not password_is_valid(request, password, verify_passwords=False): return False
    return True