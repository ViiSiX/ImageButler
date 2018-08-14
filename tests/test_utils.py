# -*- coding: utf-8 -*-

import os
import sys
import pytest
import uuid
import time
import msgpack
import piexif
from PIL import Image
from imagebutler import utils


def test_validate_email():
    """Test validate_email function."""

    valid_emails = [
        'test@test.test',
        'so.long.i.dont.care.test@te.te.te',
        'iAmS0lesS_wAnNa@B3aUt1.Fu1.lol'
    ]
    invalid_emails = [
        'invalid email bleh bleh',
        'user@mail',
        'usermail@',
        '@usermail',
        'user@mail.',
        'user@.mail',
        'user.mail@domain',
        'user.@mail',
        '.user@mail'
    ]

    for email in valid_emails:
        assert utils.validate_email(email)
    for email in invalid_emails:
        assert not utils.validate_email(email)
    with pytest.raises(TypeError):
        utils.validate_email(list)


def test_validate_mime():
    """Test validate_mime function."""

    valid_mimes = [
        'image/bmp',
        'image/png',
        'image/x-windows-bmp',
        'image/vnd.dwg'
    ]
    invalid_mimes = [
        'application/msword',
        'text/plain',
        'abc/zyz',
        'abc/image/xyz',
        'image/x/y',
        'image/x,y',
        ['image/bmp'],
        {'image/bmp'},
        ('image/bmp', 'image/png')
    ]

    for mime in valid_mimes:
        utils.validate_mime(mime)
    for mime in invalid_mimes:
        with pytest.raises(TypeError) as except_info:
            utils.validate_mime(mime)
        except_message = str(except_info.value)
        assert except_message.find('MIME should be string, not') \
            or except_message.find('Uploaded file is not an image!')


def test_generate_uuid():
    """Test generate_uuid function."""

    uuid_1 = utils.generate_uuid()
    assert uuid_1 is not None
    assert uuid_1 != ''
    assert isinstance(uuid_1, str)
    assert isinstance(uuid.UUID(uuid_1), uuid.UUID)

    assert utils.generate_uuid() != uuid_1


def test_generate_runtime():
    """Test generate_runtime function."""

    runtime = utils.generate_runtime()
    now = int(time.time()*1000)
    assert round(now - runtime) == 0


class TestTimer(object):
    """Test Timer class from Helper."""

    def test_timer(self):
        timer = utils.Timer()
        assert timer.get_total_time().find("seconds") > 0

        time.sleep(1)
        assert timer.get_total_milliseconds() > 1000
        assert timer.get_total_time().find("seconds") > 0
        assert isinstance(timer.get_total_seconds(), float)
        assert timer.get_total_seconds() > 1

        timer.spend(1)
        assert timer.get_total_time().find("minutes") > 0
        assert timer.get_total_seconds() > 60


def test_user_identity_check():
    """Test user_identity_check function."""

    class User(object):

        def __init__(self, username, password):
            self.username = username
            self.password = password

    assert utils.user_identity_check(None, 'S3cu&e')[0] == 0
    assert utils.user_identity_check(User('username', 'pw'), 'S3cu&e')[0] == 0
    assert \
        utils.user_identity_check(User('username', 'S3cu&e'), 'S3cu&e')[0] == 1


def test_get_checksum():
    """Test get_checksum function."""

    assert utils.get_checksum('aaa') == \
        b'9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0'
    assert utils.get_checksum('tôi') == \
        b'e530a4ec95132d4fdc303a4c7d42cca60d1bf78a49c1db9a7d840dff0caf0ae2'
    assert utils.get_checksum(os.urandom(10))


def test_generate_password():
    """Test generate_password function."""

    assert utils.generate_password()
    try:
        correct_instance = isinstance(utils.generate_password(),
                                      (basestring, str))
    except NameError:
        correct_instance = isinstance(utils.generate_password(),
                                      (bytes, str))
    assert correct_instance


def test_get_image_exif(sample_pil_jpeg_object_with_exif,
                        sample_pil_jpeg_object_no_exif,
                        sample_pil_png_object):
    """Test get_image_exif function to return exif data or None."""

    assert utils.get_image_exif(sample_pil_png_object) is None
    assert utils.get_image_exif(sample_pil_jpeg_object_no_exif) is None

    exif = utils.get_image_exif(sample_pil_jpeg_object_with_exif)
    assert exif
    # Ensure that the function return right format
    deserialize_exif = msgpack.unpackb(exif, use_list=False)
    assert deserialize_exif
    assert piexif.dump(deserialize_exif)


@pytest.mark.skipif(sys.version[0] == '3',
                    reason="Only for python 2.x")
def test_advance_get_image_exif_py2(sample_pil_jpeg_object_with_exif):
    """Test if exif is processed consistency. Only for Python 2.x."""

    having_exif_image = sample_pil_jpeg_object_with_exif
    ori_exif = piexif.load(having_exif_image.info['exif'])
    deserialized_exif = msgpack.unpackb(
        utils.get_image_exif(having_exif_image), use_list=False
    )
    assert deserialized_exif == ori_exif


@pytest.mark.skipif(sys.version[0] == '2',
                    reason="Only for python 3.x")
def test_advance_get_image_exif_py3(sample_pil_jpeg_object_with_exif):
    """Test if exif is processed consistency. Only for Python 3.x."""

    having_exif_image = sample_pil_jpeg_object_with_exif
    ori_exif = piexif.load(having_exif_image.info['exif'])
    deserialized_exif = msgpack.unpackb(
        utils.get_image_exif(having_exif_image), use_list=False
    )
    for k in ori_exif.keys():
        assert ori_exif[k] == deserialized_exif[k.encode()]


def test_process_uploaded_image_with_exif(
        sample_pil_jpeg_object_with_exif
):
    """Test process_uploaded_image with image having exif."""

    ret_1 = utils.process_uploaded_image(
        sample_pil_jpeg_object_with_exif,
        '1M'
    )
    assert isinstance(ret_1[0], Image.Image)
    assert ret_1[1]
    assert ret_1[2]
    assert ret_1[3] < 1 * 1024 * 1024
    assert ret_1[4]

    ret_2 = utils.process_uploaded_image(
        sample_pil_jpeg_object_with_exif,
        '512K'
    )
    # Reserve place for EXIF
    assert isinstance(ret_2[0], Image.Image)
    assert ret_2[1]
    assert ret_2[2]
    assert ret_2[3] < 512 * 1024 * 1.05
    assert ret_2[4]

    ret_3 = utils.process_uploaded_image(
        sample_pil_jpeg_object_with_exif,
        '0'
    )
    assert isinstance(ret_3[0], Image.Image)
    assert ret_3[1]
    assert ret_3[2]
    assert ret_3[4]


def test_process_uploaded_image_without_exif(
        sample_pil_jpeg_object_no_exif
):
    """Test process_uploaded_image with image not having exif."""

    ret_1 = utils.process_uploaded_image(
        sample_pil_jpeg_object_no_exif,
        '1M'
    )
    assert isinstance(ret_1[0], Image.Image)
    assert ret_1[1]
    assert ret_1[2]
    assert ret_1[3] < 1 * 1024 * 1024
    assert ret_1[4] is None

    ret_2 = utils.process_uploaded_image(
        sample_pil_jpeg_object_no_exif,
        '256K'
    )
    # Reserve place for EXIF
    assert ret_2[3] < 256 * 1024 * 1.05
    assert ret_2[4] is None
