#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'myip',
      version = '0.1',
      description = "Simply print the IP of the current host",
      author = 'Oren Held',
      author_email = 'oren@held.org.il',
      url = 'http://www.github.com/orenhe/myip',
      packages = find_packages(),
      license = 'MIT',
      entry_points = {
          'console_scripts': ['myip = myip.myip_cmd:main'],
      }
     )
