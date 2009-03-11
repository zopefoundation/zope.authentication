##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""HTTP Basic Authentication adapter

$Id$
"""
from zope.component import adapts
from zope.publisher.interfaces.http import IHTTPCredentials

from zope.authentication.loginpassword import LoginPassword


class BasicAuthAdapter(LoginPassword):
    """Adapter for handling HTTP Basic Auth."""

    adapts(IHTTPCredentials)

    def __init__(self, request):
        self.__request = request
        # TODO base64 decoding should be done here, not in request
        lpw = request._authUserPW()
        if lpw is None:
            login, password = None, None
        else:
            login, password = lpw
        super(BasicAuthAdapter, self).__init__(login, password)

    def needLogin(self, realm):
        self.__request.unauthorized('basic realm="%s"' % realm)
