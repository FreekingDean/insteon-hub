import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "insteon-hub",
    version = "0.2.1",
    author = "Dean Galvin",
    author_email = "deangalvin3@gmail.com",
    description = ("A python package that interacts with the Insteon Hub Cloud API"),
    license = "MIT",
    keywords = "insteon hub cloud",
    url = "https://github.com/FreekingDean/insteon-hub",
    packages=['insteon'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
    ],
)
