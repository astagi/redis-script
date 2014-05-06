#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="redis-script",
      py_modules=['redis-script'],
      version="0.1dev",
      description="A simple command line tool to manage your Redis scripts easily using aliases",
      license="MIT",
      author="Andrea Stagi",
      author_email="stagi.andrea@gmail.com",
      url="https://github.com/astagi/redis-script",
      keywords= "redis script commandline python lua alias",
      install_requires=[
        "redis",
      ],
      entry_points = {
        'console_scripts': [
            'redis-script = rediscript:main',
        ],
      },
      zip_safe = True)