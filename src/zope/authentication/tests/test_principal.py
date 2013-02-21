##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""Test for principal lookup related functionality
"""
import doctest
import re
import unittest
from zope.testing import renormalizing

checker = renormalizing.RENormalizing([
    # Python 3 strings remove the "u".
    (re.compile("u('.*?')"),
     r"\1"),
    (re.compile('u(".*?")'),
     r"\1"),
    ])


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.authentication.principal', checker=checker),
        doctest.DocFileSuite('../principalterms.txt', checker=checker),
        ))
