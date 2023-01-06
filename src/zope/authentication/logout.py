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
"""
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

from zope.authentication.interfaces import IAuthentication
from zope.authentication.interfaces import ILogout
from zope.authentication.interfaces import ILogoutSupported


@adapter(IAuthentication)
@implementer(ILogout)
class NoLogout:
    """
    An adapter for :class:`~.IAuthentication` utilities that don't
    implement :class:`~.ILogout`.
    """

    def __init__(self, auth):
        pass

    def logout(self, request):
        """Does nothing."""


@adapter(Interface)
@implementer(ILogoutSupported)
class LogoutSupported:
    """A class that can be registered as an adapter to flag logout support."""

    def __init__(self, dummy):
        pass
