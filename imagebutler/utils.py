import time
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

    image_re = re.compile(r'image/*')
    if image_re.match(mime):
        return
    else:
        raise TypeError('Uploaded file is not an image! (%s)'
                        % mime)


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
    Get and return exif information if it is available.

    :param image: Image object.
    :type image: PIL.Image.Image
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


def user_identity_check(user, password):
    """Check if user is not null and have exact password as the given ones."""
    if user is None:
        return 0, {'return': {'error': 'User does not existed!'}}
    if user.password != password:
        return 0, {'return': {'error': 'Authentication failed!'}}
    return 1,


def generate_runtime():
    """
    Generate an epoch timestamp in milliseconds at the this function run.

    :return: Epoch timestamp in milliseconds.
    """
    return int(time.time() * 1000)


class Timer(object):
    """
    Timer Class.
    Timer class is used to track the total runtime
    since the class construction.
    """

    def __init__(self):
        """Timer constructor, set a time object."""
        self.start_time = generate_runtime()

    def get_total_time(self):
        """Return human readable total runtime since class construction."""
        total_time = time.time() * 1000 - self.start_time

        if total_time >= 60000:
            return "{minutes} minutes {seconds} seconds".format(
                minutes=total_time / 60000,
                seconds=(total_time % 60000) / 1000
            )

        elif total_time >= 1000:
            return "{seconds} seconds".format(seconds=total_time / 1000)

        else:
            return "{milliseconds} milliseconds".\
                format(milliseconds=total_time)

    def spend(self, minutes):
        """
        Simulate of spending a number of minutes.
        :param minutes: number of minutes that has already spent.
        :return: Set the initial time of this class.
        """
        self.start_time -= 60000 * minutes

    def get_total_milliseconds(self):
        """Return total runtime since class construction in milliseconds."""
        return time.time() * 1000 - self.start_time

    def get_total_seconds(self):
        """Return total runtime since class construction in seconds."""
        return float(self.get_total_milliseconds()) / 1000
