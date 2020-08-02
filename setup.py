from distutils.core import setup
setup(
    name='twittertail',
    packages=['twittertail'],
    version='0.1',
    license='MIT',
    description='Tail a twitter account from the command line.',
    author='Nathan Davison',
    author_email='ndavison85@gmail.com',
    url='https://github.com/ndavison/twittertail',
    download_url='https://github.com/ndavison/twittertail/archive/v01.tar.gz',
    keywords=['twitter', 'tweets', 'cli'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'asyncio',
        'aiohttp',
        'colored',
    ],
)
