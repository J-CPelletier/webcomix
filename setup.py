from setuptools import setup

setup(
    name="webcomix",
    version="3.1.1",
    description="Webcomic downloader",
    long_description="webcomix is a webcomic downloader that can additionally create a .cbz file once downloaded.",
    url="https://github.com/J-CPelletier/webcomix",
    author="Jean-Christophe Pelletier",
    author_email="pelletierj97@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Framework :: Scrapy",
    ],
    packages=["webcomix"],
    install_requires=[
        "Click",
        "fake-useragent",
        "scrapy",
        "tqdm",
        "PyDispatcher",
        "scrapy-splash",
    ],
    extras_require={
        "dev": ["pytest", "pytest-cov==2.5.1", "pytest-mock", "coveralls", "pre-commit"]
    },
    python_requires=">=3.5",
    entry_points="""
        [console_scripts]
        webcomix=webcomix.cli:cli
    """,
)
