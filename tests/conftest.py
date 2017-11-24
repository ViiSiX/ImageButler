"""Setup and initialization for Unit Tests."""

import os
import pytest


test_dir = os.path.dirname(os.path.realpath(__file__)) + '/.unittest'
if not os.path.exists(test_dir):
    os.mkdir(test_dir)


def remove_file_if_existed(file_path):
    """Remove one file if it is existed!"""
    if os.path.isfile(file_path):
        return os.remove(file_path)
