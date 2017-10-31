import re
import uuid
import hashlib
from sys import version_info
from Crypto.Hash import SHA256


def validate_email(email):
    """Return if a given string is email or not."""

    try:
        return bool(
            re.search(r'^.*?@([\w\-]+\.)+[\w\-]+$', email, flags=re.IGNORECASE)
        )
    except TypeError:
        raise TypeError('Email should be string, not {0}'.format(type(email)))


def encrypt_password(password):
    """
    Encrypt the clear-text password to SHA hash.
    :param password: Password in clear text.
    :type password: str
    :return: Hashed string.
    """

    if password is None:
        raise TypeError("Password should be a string!")
    if version_info >= (3, 0):
        if not isinstance(password, str):
            raise TypeError("Password should be a string!")
    else:
        if not isinstance(password, (str, unicode)):
            raise TypeError("Password should be a string!")

    salt = uuid.uuid4().hex
    return \
        hashlib.sha512(salt.encode() + password.encode()).\
        hexdigest() + ':' + salt


def get_checksum(data):
    """
    Given data, return the checksum of that data.
    :param data:
    :return: Checksum string.
    """

    return SHA256.new(data).hexdigest()
