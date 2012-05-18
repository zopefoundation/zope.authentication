##############################################################################
#
# Copyright (c) 2004-2009 Zope Foundation and Contributors.
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
"""
Logout Test
"""
import doctest
import unittest

from zope.component import provideAdapter, adapter
from zope.interface import implementer

from zope.authentication.interfaces import IAuthentication


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            '../logout.txt',
            globs={'provideAdapter': provideAdapter,
                   'TestRequest': object,
                   'implementer': implementer,
                   'adapter': adapter,
                   'IAuthentication': IAuthentication
                  },
            ),
        ))
