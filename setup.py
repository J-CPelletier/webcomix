from setuptools import setup

setup(
    name='WebComicToCBZ',
    version=1.0,
    packages=[
        "webcomictocbz"
    ],
    install_requires=[
        'Click',
        'lxml',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        WebComicToCBZ=webcomictocbz.main:cli
    ''',
)
