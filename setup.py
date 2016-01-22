import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

REQUIRES = [
    'requests>=2,<3',
    'pyyaml>=3.11,<4'
]

setup(
    name = "insteon-hub",
    version = "0.3.0",
    author = "Dean Galvin",
    author_email = "deangalvin3@gmail.com",
    description = ("A python package that interacts with the Insteon Hub Cloud API"),
    license = "MIT",
    keywords = ["insteon", "hub", "cloud"],
    url = "https://github.com/FreekingDean/insteon-hub",
    packages=['insteon'],
    install_requires=REQUIRES,
    long_description=read('README.md'),
    classifiers=[
        'Intended Audience :: Developers',
        "Development Status :: 3 - Alpha",
        "Topic :: Home Automation",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        "License :: OSI Approved :: MIT License",
    ],
)
