#!/usr/bin/python3
from setuptools import setup
setup(
    name='twittertail',
    packages=['twittertail'],
    version='0.3',
    license='MIT',
    description='Tail a twitter account from the command line.',
    author='Nathan Davison',
    author_email='ndavison85@gmail.com',
    url='https://github.com/ndavison/twittertail',
    download_url='https://github.com/ndavison/twittertail/archive/v03.tar.gz',
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
            'twittertail=twittertail:main',
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
