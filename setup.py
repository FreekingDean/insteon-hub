import os
import re
from setuptools import setup

REQUIRES = [
    'requests>=2,<3',
    'pyyaml>=3.11,<4'
]

PACKAGE_NAME = 'insteon-hub'

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, PACKAGE_NAME.split('-')[0], 'const.py')) as fp:
    VERSION = re.search("__version__ = '([^']+)'", fp.read()).group(1)

setup(
    name = PACKAGE_NAME,
    version = VERSION,
    author = "Dean Galvin",
    author_email = "deangalvin3@gmail.com",
    description = ("A python package that interacts with the Insteon Hub Cloud API"),
    license = "MIT",
    keywords = ["insteon", "hub", "cloud"],
    url = "https://github.com/FreekingDean/insteon-hub",
    packages=['insteon'],
    include_package_data=True,
    install_requires=REQUIRES,
    classifiers=[
        'Intended Audience :: Developers',
        "Development Status :: 3 - Alpha",
        "Topic :: Home Automation",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        "License :: OSI Approved :: MIT License",
    ],
)
