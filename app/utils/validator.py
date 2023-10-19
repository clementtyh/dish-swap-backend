import re
from fastapi import HTTPException
from models.response import ErrorOut

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
    total_time_pattern = "^(?:[1-9]\d{0,2}|1[0-3]\d{2}|14[0-3][0-9]|143[0-9])$"
    if not re.match(total_time_pattern, value):
        return False
    return True

def validate_difficulty(value: str):
    allowed_difficulties = ["easy", "medium", "hard"]
    if value.lower() not in allowed_difficulties:
        return False
    return True

def validate_servings(value: str):
    servings_pattern = "^(?:[1-9]|[1-9]\d)$"
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

def validate_required(field_name, value):
    if not value or all(field_name is None or not field_name.strip() for field_name in value):
        raise HTTPException(
            status_code=400,
            detail=ErrorOut(message=f"{field_name} is required").model_dump())

def validate_required_integer(field_name, value):
    if value is None or not str(value).strip():
        raise HTTPException(
            status_code=400,
            detail=ErrorOut(message=f"{field_name} is required").model_dump())

def validate_integer(field_name, value):
    try:
        return int(value)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=ErrorOut(message=f"{field_name} must be a valid integer").model_dump()
        )

def validate_invalid(field_name, value, validate_func=None):
    if validate_func and not validate_func(value):
        raise HTTPException(
            status_code=400, 
            detail=ErrorOut(message=f"Invalid {field_name} '{value}'").model_dump()
        )
    
def validate_max_images(field_name, value):
    max_image_count = 15
    if not validate_max_length(value, max_image_count):
        raise HTTPException(
            status_code=400,
            detail=ErrorOut(message=f"Exceeded maximum {field_name} count of {max_image_count}").model_dump()
        )