##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Terms view for Principal Source

$Id$
"""
__docformat__ = "reStructuredText"

from zope.component import getUtility, adapts
from zope.interface import implements
from zope.browser.interfaces import ITerms
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.app.security.interfaces import IAuthentication, IPrincipalSource

class Term(object):

    def __init__(self, token, title):
        self.token = token
        self.title = title


class PrincipalTerms(object):
    implements(ITerms)
    adapts(IPrincipalSource, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context

    def getTerm(self, principal_id):
        if principal_id not in self.context:
            raise LookupError(principal_id)

        auth = getUtility(IAuthentication)
        principal = auth.getPrincipal(principal_id)

        if principal is None:
            raise LookupError(principal_id)

        return Term(principal_id.encode('base64').strip().replace('=', '_'),
                    principal.title)

    def getValue(self, token):
        return token.replace('_', '=').decode('base64')
