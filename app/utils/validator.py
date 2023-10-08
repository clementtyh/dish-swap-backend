import re
from datetime import datetime

def validate_password(value: str):
    password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.match(password_pattern, value):
        return False
    return True


def validate_email(value: str):
    email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, value):
        return False
    return True


def validate_display_name(value: str):
    display_name_pattern = "^[a-zA-Z_][a-zA-Z0-9_]{0,49}$"
    if not re.match(display_name_pattern, value):
        return False
    return True


def validate_jwt_token(value: str):
    jwt_token_pattern = "^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$"
    if not re.match(jwt_token_pattern, value):
        return False
    return True


def validate_filename(value: str):
    file_name_pattern = "(?i)^(.*\.(png|jpg|jpeg))$"
    if not re.match(file_name_pattern, value):
        return False
    return True


def validate_content_type(value: str):
    content_type_pattern = "(?i)^(image\/(jpeg|jpg|png))$"
    if not re.match(content_type_pattern, value):
        return False
    return True


def validate_alphanumeric_symbols(value: str):
    alphanumeric_symbols_pattern = "^[a-zA-Z0-9!@#$%^&*]+$"
    if not re.match(alphanumeric_symbols_pattern, value):
        return False
    return True

def validate_recipe_name(value: str):
    recipe_name_pattern = "^[a-zA-Z0-9\s]{1,50}$"
    if not re.match(recipe_name_pattern, value):
        return False
    return True

def validate_description(value: str):
    min_length = 1
    max_length = 500
    if not validate_length_range(value, min_length, max_length):
        return False
    return True

def validate_ingredient(value: str):
    min_length = 2
    max_length = 200
    if not validate_length_range(value, min_length, max_length):
        return False
    return True

def validate_step(value: str):
    min_length = 10
    max_length = 500
    if not validate_length_range(value, min_length, max_length):
        return False
    return True

def validate_total_time(value: str):
    total_time_pattern = "^\d{1,3}$"
    if not re.match(total_time_pattern, value):
        return False
    return True

def validate_difficulty(value: str):
    allowed_difficulties = ["easy", "medium", "hard"]
    if value.lower() not in allowed_difficulties:
        return False
    return True

def validate_servings(value: str):
    servings_pattern = "^\d{1,2}$"
    if not re.match(servings_pattern, value):
        return False
    return True

def validate_file_size(value: int):
    max_file_size = 10 * 1024 * 1024 ## 10 MB
    if not validate_max_length(value, max_file_size):
        return False
    return True

def validate_max_length(value: int, max_length: int):
    return value <= max_length

def validate_length_range(value: str, min_length: int, max_length: int):
    return min_length <= len(value) <= max_length