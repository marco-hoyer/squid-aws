#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'squid-dynamodb',
          version = '0.1',
          description = '''squid-dynamodb''',
          long_description = '''Make squid a dynamic proxy by gathering auth information and acl from dynamodb
''',
          author = "Marco Hoyer",
          author_email = "marco.hoyer@immobilienscout24.de",
          license = 'GNU GPL v3',
          url = 'https://vcs.rz.is/svn/prod/source/squid-dynamodb/',
          scripts = ['scripts/squid-dynamodb-auth.py'],
          packages = ['squid_dynamodb', 'squid_dynamodb.providers'],
          classifiers = ['Development Status :: 3 - Alpha', 'Programming Language :: Python'],
             #  data files
             # package data
          install_requires = [ "boto" ],
          
          zip_safe=True
    )
