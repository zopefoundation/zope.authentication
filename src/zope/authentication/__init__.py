##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Zope Application-specific Security code

$Id$
"""
from zope.component import adapts
from zope.interface import implements, Interface
from zope.app.security import interfaces


class LogoutSupported(object):
    """A class that can be registered as an adapter to flag logout support."""

    adapts(Interface)

    implements(interfaces.ILogoutSupported)

    def __init__(self, dummy):
        pass


class NoLogout(object):
    """An adapter for IAuthentication utilities that don't implement ILogout."""

    adapts(interfaces.IAuthentication)

    implements(interfaces.ILogout)

    def __init__(self, auth):
        pass

    def logout(self, request):
        pass
