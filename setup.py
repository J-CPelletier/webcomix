from setuptools import setup
from main import __version__

setup(
    name='WebComicToCBZ',
    version=__version__,
    py_modules=['WebComicToCBZ',
    'comic'],
    install_requires=[
        'Click',
        'lxml',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        WebComicToCBZ=main:cli
    ''',
)
