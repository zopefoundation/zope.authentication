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
"""Principal source and helper function
"""
from zope.browser.interfaces import ITerms
from zope.component import getUtility, queryNextUtility, adapter
from zope.interface import implementer, Interface
from zope.schema.interfaces import ISourceQueriables

from zope.authentication.interfaces import IAuthentication, IPrincipalSource
from zope.authentication.interfaces import PrincipalLookupError


def checkPrincipal(context, principal_id):
    """An utility function to check if there's a principal for given principal id.
    
    Raises ValueError when principal doesn't exists for given context and
    principal id.

    To test it, let's create and register a dummy authentication utility.
    
      >>> @implementer(IAuthentication)
      ... class DummyUtility:
      ...
      ...     def getPrincipal(self, id):
      ...         if id == 'bob':
      ...             return id
      ...         raise PrincipalLookupError(id)

      >>> from zope.component import provideUtility
      >>> provideUtility(DummyUtility())

    Now, let's the behaviour of this function.
    
      >>> checkPrincipal(None, 'bob')
      >>> checkPrincipal(None, 'dan')
      Traceback (most recent call last):
      ...
      ValueError: ('Undefined principal id', 'dan')
    
    """
    auth = getUtility(IAuthentication, context=context)
    try:
        if auth.getPrincipal(principal_id):
            return
    except PrincipalLookupError:
        pass
    raise ValueError("Undefined principal id", principal_id)


@implementer(IPrincipalSource, ISourceQueriables)
class PrincipalSource(object):
    """Generic Principal Source"""

    def __contains__(self, id):
        """Test for the existence of a user.

        We want to check whether the system knows about a particular
        principal, which is referenced via its id. The source will go through
        the most local authentication utility to look for the
        principal. Whether the utility consults other utilities to give an
        answer is up to the utility itself.

        First we need to create a dummy utility that will return a user, if
        the id is 'bob'.

        >>> @implementer(IAuthentication)
        ... class DummyUtility:
        ...     def getPrincipal(self, id):
        ...         if id == 'bob':
        ...             return id
        ...         raise PrincipalLookupError(id)

        Let's register our dummy auth utility.

        >>> from zope.component import provideUtility
        >>> provideUtility(DummyUtility())

        Now initialize the principal source and test the method

        >>> source = PrincipalSource()
        >>> 'jim' in source
        False
        >>> 'bob' in source
        True
        """
        auth = getUtility(IAuthentication)
        try:
            auth.getPrincipal(id)
        except PrincipalLookupError:
            return False
        else:
            return True

    def getQueriables(self):
        """Returns an iteratable of queriables.

        Queriables are responsible for providing interfaces to search for
        principals by a set of given parameters (can be different for the
        various queriables). This method will walk up through all of the
        authentication utilities to look for queriables.

        >>> @implementer(IAuthentication)
        ... class DummyUtility1:
        ...     __parent__ = None
        ...     def __repr__(self): return 'dummy1'
        >>> dummy1 = DummyUtility1()

        >>> @implementer(ISourceQueriables, IAuthentication)
        ... class DummyUtility2:
        ...     __parent__ = None
        ...     def getQueriables(self):
        ...         return ('1', 1), ('2', 2), ('3', 3)
        >>> dummy2 = DummyUtility2()

        >>> @implementer(IAuthentication)
        ... class DummyUtility3(DummyUtility2):
        ...     def getQueriables(self):
        ...         return ('4', 4),
        >>> dummy3 = DummyUtility3()

        >>> from zope.authentication.tests.utils import testingNextUtility
        >>> testingNextUtility(dummy1, dummy2, IAuthentication)
        >>> testingNextUtility(dummy2, dummy3, IAuthentication)

        >>> from zope.component import provideUtility
        >>> provideUtility(dummy1)

        >>> source = PrincipalSource()
        >>> list(source.getQueriables())
        [(u'0', dummy1), (u'1.1', 1), (u'1.2', 2), (u'1.3', 3), (u'2.4', 4)]
        """
        i = 0
        auth = getUtility(IAuthentication)
        yielded = []
        while True:
            queriables = ISourceQueriables(auth, None)
            if queriables is None:
                yield unicode(i), auth
            else:
                for qid, queriable in queriables.getQueriables():
                    # ensure that we dont return same yielded utility more
                    # then once
                    if queriable not in yielded:
                        yield unicode(i)+'.'+unicode(qid), queriable
                        yielded.append(queriable)
            auth = queryNextUtility(auth, IAuthentication)
            if auth is None:
                break
            i += 1


@implementer(ITerms)
@adapter(IPrincipalSource, Interface)
class PrincipalTerms(object):


    def __init__(self, context, request):
        self.context = context

    def getTerm(self, principal_id):
        if principal_id not in self.context:
            raise LookupError(principal_id)

        auth = getUtility(IAuthentication)
        principal = auth.getPrincipal(principal_id)

        if principal is None:
            # TODO: is this a possible case?
            raise LookupError(principal_id)

        return PrincipalTerm(principal_id.encode('base64').strip().replace('=', '_'),
                             principal.title)

    def getValue(self, token):
        return token.replace('_', '=').decode('base64')


class PrincipalTerm(object):

    def __init__(self, token, title):
        self.token = token
        self.title = title
