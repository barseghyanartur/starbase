import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'readme.rst')).read()
except:
  readme = ''

version = '0.1'

setup(
    name = 'starbase',
    version = version,
    description = ("Python client for HBase Stargate REST server"),
    long_description = readme,
    classifiers = [
        "Programming Language :: Python",
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = 'hadoop, hbase, stargate, app, python',
    author = 'Artur Barseghyan',
    author_email = 'artur.barseghyan@gmail.com',
    license = 'GPL 2.0/LGPL 2.1',
    url = 'https://github.com/barseghyanartur/starbase',
    package_dir = {'':'src'},
    packages = find_packages(where='./src'),
    include_package_data = True,
    install_requires = [
        'requests==1.2.3',
        'ordereddict==1.1',
        'lxml==3.2.1',
        'simple-timer==0.1'
        ]
)
