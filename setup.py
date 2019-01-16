import os
import re

from setuptools import find_packages
from setuptools import setup


BASE_NAME = 'ceda_opensearch'

V_FILE = open(os.path.join(os.path.dirname(__file__),
                           BASE_NAME, '__init__.py'))

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(V_FILE.read()).group(1)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=BASE_NAME,
    version=VERSION,
    author=u'Antony Wilson',
    author_email='antony.wilson@stfc.ac.uk',
    include_package_data=True,
    packages=find_packages(),
    url='http://stfc.ac.uk/',
    license='BSD licence',
    long_description=README,

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],

    # Adds dependencies
    install_requires=[
        'Django==1.11.18',
        'ceda-markup==0.2.0',
        'elasticsearch_dsl==6.1.0'
    ],
)
