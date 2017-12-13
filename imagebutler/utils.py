import time
import re
import uuid
import base64
import pickle
import piexif
from PIL import Image
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

    image_re = re.compile(r'^image/[\w\-.]+$')
    try:
        if image_re.match(mime):
            return
        else:
            raise TypeError(
                'Uploaded file is not an image! ({0})'.format(mime)
            )
    except TypeError:
        raise TypeError('MIME should be string, not {0}'.format(type(mime)))


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
    :return: exif data or None.
    """

    try:
        exif = image.info['exif']

        serialized_exif = \
            pickle.dumps(piexif.load(exif), pickle.HIGHEST_PROTOCOL)
        return serialized_exif

    except KeyError:
        return None


def process_uploaded_image(image, max_size=0):
    """
    Process uploaded and return necessary information.

    For resizing old image, we don't do it now but maybe in later releases.
    :param image: Image object.
    :type image: Image.Image
    :param max_size: max size from the configuration
    :type max_size: str
    :return: a tuple of processed image information.
    """

    image_sio = BytesIO()
    image_exif = get_image_exif(image)
    if image_exif:
        image_exif_deserialized = pickle.loads(image_exif)
        image.save(image_sio, format=image.format,
                   exif=piexif.dump(image_exif_deserialized)
                   )
    else:
        image_exif_deserialized = None
        image.save(image_sio, format=image.format)
    image_size = len(image_sio.getvalue())
    image_dimension_size = image.size

    # TODO: Move this to a utils function
    max_size = str(max_size)
    matched_config = re.match(r'^(\d+)M$', max_size)
    if matched_config:
        max_size = int(matched_config.group(1)) * 1024 * 1024
    else:
        matched_config = re.match(r'^(\d+)K$', max_size)
        if matched_config:
            max_size = int(matched_config.group(1)) * 1024
        else:
            max_size = 0

    if 0 < max_size < image_size:
        resize_ratio = (float(max_size) / image_size) ** 0.5
        new_dimension_size = (
            int(image_dimension_size[0] * resize_ratio),
            int(image_dimension_size[1] * resize_ratio)
        )
        print(max_size, image_size, resize_ratio)
        image.thumbnail(new_dimension_size, Image.ANTIALIAS)
        image_dimension_size = image.size
        image_sio.close()
        image_sio = BytesIO()
        if image_exif:
            image_exif_deserialized["0th"][piexif.ImageIFD.XResolution] = (
                image_dimension_size[0], 1
            )
            image_exif_deserialized["0th"][piexif.ImageIFD.YResolution] = (
                image_dimension_size[1], 1
            )
            image.save(image_sio, format=image.format,
                       exif=piexif.dump(image_exif_deserialized))
        else:
            image.save(image_sio, format=image.format)
        image_size = len(image_sio.getvalue())

    image_file_content = image_sio.getvalue()
    image_checksum = get_checksum(image_file_content)
    image_sio.close()

    return image, image_file_content, image_checksum, image_size, image_exif


def user_identity_check(user, password):
    """
    Check if user is not null and have exact password as the given ones.

    For now we just store the plain text password, do not need to hash it.
    :param user: object that have username and password attribute.
    :type user: models.UserModel
    :param password: plaintext password string.
    :type password: str
    """

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
