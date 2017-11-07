import re
import uuid
import base64
from Crypto import Random
from Crypto.Hash import SHA256


def validate_email(email):
    """Return if a given string is email or not."""

    try:
        return bool(
            re.search(r'^.*?@([\w\-]+\.)+[\w\-]+$', email, flags=re.IGNORECASE)
        )
    except TypeError:
        raise TypeError('Email should be string, not {0}'.format(type(email)))


def generate_user_name():
    """Return an UUID string as new user name."""

    return str(uuid.uuid4())


def generate_password():
    """Return a password string."""

    rng = Random.new().read
    return base64.b64encode(rng(96)).decode('ascii')


def get_checksum(data):
    """
    Given data, return the checksum of that data.
    :param data:
    :return: Checksum string.
    """

    return SHA256.new(data).hexdigest()
