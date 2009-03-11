##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.authentication package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.authentication',
      version = '3.7.0dev',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Definition of authentication basics for Zope Framework',
      long_description=(
          read('README.txt')
          + '\n\n' +
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('src', 'zope', 'authentication', 'logout.txt')
          + '\n\n' +
          read('src', 'zope', 'authentication', 'principalterms.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope security authentication",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.authentication',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      install_requires=['setuptools',
                        'zope.browser',
                        'zope.component',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.schema',
                        
                        'zope.publisher', # XXX: this is for ILoginPassword
                                          # adapters that should be moved
                                          # elsewhere, probably to zope.publisher

                        'zope.site', # XXX: this shouldn't be needed
                        'zope.app.component', # XXX: this is for testing, until
                        'zope.app.testing',   # we got testingNextUtility in
                                              # a sane place or rewrite tests.
                        ],
      include_package_data = True,
      zip_safe = False,
      )