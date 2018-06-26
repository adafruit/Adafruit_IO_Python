from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages
import re

VERSIONFILE="_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
print('version: ', verstr)

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: MacOS',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(
    name             = 'adafruit-io',
    version          =  verstr,
    author           = 'Justin Cooper',
    author_email     = 'justin@adafruit.com',
    packages         = ['Adafruit_IO'],
    py_modules       = ['ez_setup'],
    url              = 'https://github.com/adafruit/io-client-python',
    license          = 'MIT',
    keywords         = 'Adafruit IO',
    classifiers      = classifiers,
    description      = 'Client library for Adafruit IO (http://io.adafruit.com/).',
    long_description = open('README.md').read(),
    install_requires = ["requests", "paho-mqtt"]
)
