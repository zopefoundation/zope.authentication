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
"""Login/Password provider.
"""
from zope.interface import implementer

from zope.authentication.interfaces import ILoginPassword


@implementer(ILoginPassword)
class LoginPassword:
    """Basic :class:`zope.authentication.interfaces.ILoginPassword`
    implementation.

    This class can be used as a base for implementing ILoginPassword adapters.
    """

    def __init__(self, login, password):
        self.__login = login
        if login is None:
            self.__password = None
        else:
            self.__password = password or ''

    def getLogin(self):
        return self.__login

    def getPassword(self):
        return self.__password

    def needLogin(self, realm):
        pass
