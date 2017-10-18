from setuptools import setup

setup(
    name='webcomix',
    version=1.1,
    packages=[
        "webcomix"
    ],
    install_requires=[
        'Click',
        'lxml',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        webcomix=webcomix.main:cli
    ''',
)
