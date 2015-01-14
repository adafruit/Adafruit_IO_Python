from setuptools import setup

setup(
    name='Adafruit_IO',
    version='0.0.1',
    author='Justin Cooper',
    author_email='justin@adafruit.com',
    packages=['Adafruit_IO'],
    url='http://pypi.python.org/pypi/adafruit_io/',
    license='LICENSE.txt',
    description='IO Client library for io.adafruit.com',
    long_description=open('README.md').read(),
    install_requires=[
        "apiclient >= 1.0.2"
    ],
)