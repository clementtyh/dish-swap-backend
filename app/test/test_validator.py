import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

# Now you can import your modules
from utils.validator import validate_password, validate_email, validate_display_name, validate_jwt_token, validate_filename, validate_content_type


# Test cases for validate_password function
def test_validate_password_valid():
    assert validate_password("StrongP@ss1") is True

def test_validate_password_too_short():
    assert validate_password("Short1") is False

def test_validate_password_no_special_character():
    assert validate_password("NoSpecial123") is False

def test_validate_password_no_digit():
    assert validate_password("NoDigit@Special") is False

def test_validate_password_no_lowercase():
    assert validate_password("UPPER123@SPECIAL") is False

def test_validate_password_no_uppercase():
    assert validate_password("lower123@special") is False

def test_validate_password_no_special_character():
    assert validate_password("NoSpecial1234") is False

def test_validate_password_valid_special_characters():
    assert validate_password("Valid@Special1") is True

def test_validate_password_whitespace():
    assert validate_password("Password With Spaces1@") is False

def test_validate_password_valid_length():
    assert validate_password("V@lidL3ngth") is True


# Test cases for validate_email function
def test_validate_email_valid():
    assert validate_email("test@example.com") is True

def test_validate_email_invalid():
    assert validate_email("invalid-email") is False

def test_validate_email_invalid_characters():
    assert validate_email("user&@example.com") is False

def test_validate_email_missing_at_symbol():
    assert validate_email("userexample.com") is False

def test_validate_email_valid_multiple_periods():
    assert validate_email("user.name@example.com") is True


# Test cases for validate_display_name function
def test_validate_display_name_valid():
    assert validate_display_name("user_name123") is True

def test_validate_display_name_invalid():
    assert validate_display_name("invalid display name") is False

def test_validate_display_name_valid_with_underscore():
    assert validate_display_name("user_name_123") is True

def test_validate_display_name_invalid_starts_with_digit():
    assert validate_display_name("1username") is False

def test_validate_display_name_valid_max_length():
    assert validate_display_name("a" * 50) is True

def test_validate_display_name_invalid_max_length():
    assert validate_display_name("a" * 51) is False


# Test cases for validate_jwt_token function
def test_validate_jwt_token_valid():
    assert validate_jwt_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c") is True

def test_validate_jwt_token_invalid():
    assert validate_jwt_token("invalid_token") is False

def test_validate_jwt_token_missing_parts():
    assert validate_jwt_token("part1.part2") is False

def test_validate_jwt_token_invalid_characters():
    assert validate_jwt_token("invalid_token!@#$%^") is False

def test_validate_jwt_token_valid_with_padding():
    assert validate_jwt_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.") is True


# Test cases for validate_filename function
def test_validate_filename_valid():
    assert validate_filename("image.jpg") is True

def test_validate_filename_invalid_extension():
    assert validate_filename("document.pdf") is False

def test_validate_filename_valid_case_insensitive():
    assert validate_filename("image.JPG") is True

def test_validate_filename_invalid_no_extension():
    assert validate_filename("no_extension") is False

def test_validate_filename_valid_extensions():
    valid_extensions = ["image.jpg", "image.png", "image.jpeg"]
    for filename in valid_extensions:
        assert validate_filename(filename) is True

def test_validate_filename_invalid_extensions():
    invalid_extensions = ["file.exe", "data.csv", "script.js", "config.yml"]
    for filename in invalid_extensions:
        assert validate_filename(filename) is False


# Test cases for validate_content_type function
def test_validate_content_type_valid():
    assert validate_content_type("image/jpeg") is True

def test_validate_content_type_invalid():
    assert validate_content_type("application/pdf") is False

def test_validate_content_type_valid_case_insensitive():
    assert validate_content_type("image/JPEG") is True

def test_validate_content_type_invalid_wrong_type():
    assert validate_content_type("video/mp4") is False

def test_validate_content_type_valid_extensions():
    valid_extensions = ["image/jpeg", "image/png"]
    for content_type in valid_extensions:
        assert validate_content_type(content_type) is True

def test_validate_content_type_invalid_extensions():
    invalid_extensions = ["video/mp4", "text/plain", "application/javascript", "audio/wav"]
    for content_type in invalid_extensions:
        assert validate_content_type(content_type) is False