import re
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('imagebutler/__init__.py', 'rb') as f:
    version = str(_version_re.search(f.read().decode('utf-8')).group(1))


setup(
    name='ImageButler',
    version=version,
    author='Trong-Nghia Nguyen',
    author_email='nghia@viisix.space',
    description='Simple images serving service,',
    packages=['imagebutler'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Restful',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'pycrypto'
    ]
)
