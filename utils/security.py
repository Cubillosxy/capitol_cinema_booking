from django.conf import settings


def add_salt_to_password(password):
    secret_key = settings.SALT_KEY
    salted_password = f"{secret_key}{password}"

    return salted_password
