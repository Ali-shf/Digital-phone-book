import re


def phone_validator(phone_number: str) -> bool:
    pattern = r"(09)\d{9}"
    return bool(re.fullmatch(pattern, phone_number))


def name_validator(name: str) -> bool:
    pattern = r"[a-zA-Z]{2,}$"
    return bool(re.fullmatch(pattern, name))


def email_validator(email: str) -> bool:
    pattern = r"^[\w\.\_]+@[\w]+\.[a-z]{2,3}$"
    return bool(re.fullmatch(pattern, email))


