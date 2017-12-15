"""Setup and initialization for Unit Tests."""

import os
import pytest
from PIL import Image


project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
test_dir = os.path.dirname(os.path.realpath(__file__)) + '/.unittest'
if not os.path.exists(test_dir):
    os.mkdir(test_dir)

static_dir = os.path.dirname(os.path.realpath(__file__)) + '/static'


def remove_file_if_existed(file_path):
    """Remove one file if it is existed!"""
    if os.path.isfile(file_path):
        return os.remove(file_path)


@pytest.fixture
def source_code_dir():
    """Return the path of the current source code."""
    return project_dir + '/imagebutler'


@pytest.fixture
def sample_pil_jpeg_object_no_exif():
    """Return a Image object of static/bitexco.jpg, no exif."""
    return Image.open(static_dir + '/bitexco.jpg')


@pytest.fixture
def sample_pil_jpeg_object_with_exif():
    """Return a Image object of static/flower.jpg, with exif."""
    return Image.open(static_dir + '/flower.jpg')


@pytest.fixture
def sample_pil_png_object():
    """Return a Image object of static/image-butler.png."""
    return Image.open(static_dir + '/image-butler.png')
