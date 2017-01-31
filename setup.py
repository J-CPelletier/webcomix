from setuptools import setup

setup(
    name='WebComicToCBZ',
    version=0.1,
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
