#!/usr/bin/python3
from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='twittertail',
    packages=['twittertail'],
    version='0.7',
    license='MIT',
    description='Tail a twitter account from the command line.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nathan Davison',
    author_email='ndavison85@gmail.com',
    url='https://github.com/ndavison/twittertail',
    download_url='https://github.com/ndavison/twittertail/archive/v07.tar.gz',
    keywords=['twitter', 'tweets', 'cli'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'asyncio',
        'aiohttp',
        'colored',
    ],
    entry_points={
        'console_scripts': [
            'twittertail=twittertail.__main__:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
