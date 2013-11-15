import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
  readme = ''

version = '0.2.5'

setup(
    name = 'starbase',
    version = version,
    description = ("Python client for HBase Stargate REST server"),
    long_description = readme,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Database",
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
        'six>=1.1.0',
        'ordereddict==1.1',
        'requests==1.2.3',
        'simple-timer==0.1',
    ]
)
