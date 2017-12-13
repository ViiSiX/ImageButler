import io
import re
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('imagebutler/__init__.py', 'rb') as f:
    version = str(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)).replace('\'', '')
with io.open('README.rst', encoding='utf-8') as f:
    description = f.read()
with io.open('HISTORY.rst', encoding='utf-8') as f:
    description += "\n\n%s" % f.read()


setup(
    name='ImageButler',
    version=version,
    author='Trong-Nghia Nguyen',
    author_email='nghia@viisix.space',
    url='https://viisix.space/projects/image-butler/',
    description='Simple images serving service,',
    long_description=description,
    packages=['imagebutler', 'imagebutler.apis'],
    entry_points="""
        [flask.commands]
        user=imagebutler.commands:user
        image=imagebutler.commands:image 
    """,
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Cors',
        'Flask-Restful',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-Redislite',
        'Flask-Login',
        'pycrypto',
        'Pillow',
        'progressbar2',
        'piexif'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6'
    ]
)
