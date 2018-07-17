"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re


# Get the version string from _version.py
verstrline = open('Adafruit_IO/_version.py', "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
print('version: ', verstr)

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: POSIX :: Linux',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: MacOS',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Topic :: Home Automation',
               'Topic :: Software Development']

setup(
    name             = 'adafruit-io',
    use_scm_version  =  True,
    setup_requires   =  ['setuptools_scm'],

    description      = 'Python client library for Adafruit IO (http://io.adafruit.com/).',
    long_description = open('README.rst').read(),
    long_description_content_type='text/x-rst',

    url              = 'https://github.com/adafruit/io-client-python',

    author           = 'Adafruit Industries',
    author_email     = 'adafruitio@adafruit.com',

    license          = 'MIT',


    version          =  verstr,
    install_requires = ["requests", "paho-mqtt"],


    packages         = ['Adafruit_IO'],
    py_modules       = ['ez_setup'],
    keywords         = 'adafruitio io python circuitpython raspberrypi hardware MQTT',
    classifiers      = classifiers
)
