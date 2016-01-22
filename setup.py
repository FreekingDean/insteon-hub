import os
from setuptools import setup

setup(
    name = "insteon-hub",
    version = "0.3.0",
    author = "Dean Galvin",
    author_email = "deangalvin3@gmail.com",
    description = ("A python package that interacts with the Insteon Hub Cloud API"),
    license = "MIT",
    keywords = "insteon hub cloud",
    url = "https://github.com/FreekingDean/insteon-hub",
    packages=['insteon'],
    long_description=read('README.md').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
    ],
)
