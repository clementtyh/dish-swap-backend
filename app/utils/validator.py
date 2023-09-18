import re

def validate_password(value: str):
    password_pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.match(password_pattern, value):
        return False
    return True


def validate_email(value: str):
    email_pattern = "^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, value):
        return False
    return True


def validate_display_name(value: str):
    display_name_pattern = "^[a-zA-Z0-9_-]+$"
    if not re.match(display_name_pattern, value):
        return False
    return True


def validate_jwt_token(value: str):
    display_name_pattern = "^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$"
    if not re.match(display_name_pattern, value):
        return False
    return True


def validate_filename(value: str):
    display_name_pattern = "(?i)^(.*\.(png|jpg|jpeg))$"
    if not re.match(display_name_pattern, value):
        return False
    return True


def validate_content_type(value: str):
    display_name_pattern = "(?i)^(image\/(jpeg|png))$"
    if not re.match(display_name_pattern, value):
        return False
    return True


def validate_alphanumeric_symbols(value: str):
    display_name_pattern = "^[a-zA-Z0-9!@#$%^&*]+$"
    if not re.match(display_name_pattern, value):
        return False
    return True
