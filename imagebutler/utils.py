import re
import uuid
import base64
import pickle
from io import BytesIO
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


def validate_mime(mime):
    """Raise exception if MIME does not match image/*."""

    image_re = re.compile('image/*')
    if image_re.match(mime):
        return
    else:
        raise TypeError('Uploaded file is not an image!')


def generate_uuid():
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
    try:
        return SHA256.new(data).hexdigest()
    except TypeError:
        data = data.encode('utf-8')
        return get_checksum(data)


def get_image_exif(image):
    """

    :param image:
    :return:
    """

    try:
        exif = image._get_exif()  # There is not public method for this.

        if exif is not None:
            exif_io = BytesIO()
            pickle.dump(exif, exif_io, pickle.HIGHEST_PROTOCOL)
            exif_data = exif_io.getvalue()
            exif_io.close()
            return exif_data

        return None
    except AttributeError:
        return None
