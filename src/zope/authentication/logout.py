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
"""ILogout implementations

$Id$
"""
from zope.component import adapts
from zope.interface import implements, Interface

from zope.authentication.interfaces import IAuthentication
from zope.authentication.interfaces import ILogout, ILogoutSupported


class NoLogout(object):
    """An adapter for IAuthentication utilities that don't implement ILogout."""

    adapts(IAuthentication)
    implements(ILogout)

    def __init__(self, auth):
        pass

    def logout(self, request):
        pass


class LogoutSupported(object):
    """A class that can be registered as an adapter to flag logout support."""

    adapts(Interface)
    implements(ILogoutSupported)

    def __init__(self, dummy):
        pass
