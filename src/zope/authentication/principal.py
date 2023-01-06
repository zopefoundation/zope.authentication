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
import base64

from zope.browser.interfaces import ITerms
from zope.component import adapter
from zope.component import getUtility
from zope.component import queryNextUtility
from zope.interface import Interface
from zope.interface import implementer
from zope.schema.interfaces import ISourceQueriables

from zope.authentication.interfaces import IAuthentication
from zope.authentication.interfaces import IPrincipalSource
from zope.authentication.interfaces import PrincipalLookupError


def checkPrincipal(context, principal_id):
    """Utility function to check if there's a principal for given principal id.

    Raises :exc:`ValueError` when principal doesn't exists for given context
    and principal id.

    To test it, let's create and register a dummy authentication utility.

      >>> from zope.authentication.interfaces import IAuthentication
      >>> from zope.authentication.interfaces import PrincipalLookupError
      >>> from zope.interface import implementer
      >>> @implementer(IAuthentication)
      ... class DummyUtility(object):
      ...
      ...     def getPrincipal(self, id):
      ...         if id == 'bob':
      ...             return id
      ...         raise PrincipalLookupError(id)

      >>> from zope.component import provideUtility
      >>> provideUtility(DummyUtility())

    Now, let's check the behaviour of this function.

      >>> from zope.authentication.principal import checkPrincipal
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
class PrincipalSource:
    """Generic Principal Source

    Implements :class:`zope.authentication.interfaces.IPrincipalSource`
    and :class:`zope.schema.interfaces.ISourceQueriables`.
    """

    def __contains__(self, id):
        """Test for the existence of a user.

        We want to check whether the system knows about a particular
        principal, which is referenced via its id. The source will go through
        the most local authentication utility to look for the
        principal. Whether the utility consults other utilities to give an
        answer is up to the utility itself.

        First we need to create a dummy utility that will return a user, if
        the id is 'bob'.

        >>> from zope.authentication.interfaces import IAuthentication
        >>> from zope.interface import implementer
        >>> @implementer(IAuthentication)
        ... class DummyUtility(object):
        ...     def getPrincipal(self, id):
        ...         if id == 'bob':
        ...             return id
        ...         raise PrincipalLookupError(id)

        Let's register our dummy auth utility.

        >>> from zope.component import provideUtility
        >>> provideUtility(DummyUtility())

        Now initialize the principal source and test the method

        >>> from zope.authentication.principal import PrincipalSource
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

        >>> from zope.schema.interfaces import ISourceQueriables
        >>> @implementer(IAuthentication)
        ... class DummyUtility1(object):
        ...     __parent__ = None
        ...     def __repr__(self): return 'dummy1'
        >>> dummy1 = DummyUtility1()

        >>> @implementer(ISourceQueriables, IAuthentication)
        ... class DummyUtility2(object):
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

        >>> from zope.authentication.principal import PrincipalSource
        >>> source = PrincipalSource()
        >>> list(source.getQueriables())
        [('0', dummy1), ('1.1', 1), ('1.2', 2), ('1.3', 3), ('2.4', 4)]
        """
        i = 0
        auth = getUtility(IAuthentication)
        yielded = []
        while True:
            queriables = ISourceQueriables(auth, None)
            if queriables is None:
                yield str(i), auth
            else:
                for qid, queriable in queriables.getQueriables():
                    # ensure that we dont return same yielded utility more
                    # then once
                    if queriable not in yielded:
                        yield f'{i}.{qid}', queriable
                        yielded.append(queriable)
            auth = queryNextUtility(auth, IAuthentication)
            if auth is None:
                break
            i += 1


@implementer(ITerms)
@adapter(IPrincipalSource, Interface)
class PrincipalTerms:
    """
    Implementation of :class:`zope.browser.interfaces.ITerms` given a
    :class:`zope.authentication.interfaces.IPrincipalSource` and
    request object.
    """

    def __init__(self, context, request):
        self.context = context

    def _encode(self, id):
        # principal_id is always str:
        id = id.encode('utf-8')

        res = base64.b64encode(id).strip().replace(b'=', b'_')
        return res.decode()

    def _decode(self, token):
        return base64.b64decode(
            token.replace('_', '=').encode()).decode('utf-8')

    def getTerm(self, principal_id):
        """Return a :class:`PrincipalTerm` for the given ID.

        If no such principal can be found, raises :exc:`LooupError`.
        """
        if principal_id not in self.context:
            raise LookupError(principal_id)

        auth = getUtility(IAuthentication)
        principal = auth.getPrincipal(principal_id)

        if principal is None:
            # TODO: is this a possible case?
            raise LookupError(principal_id)

        return PrincipalTerm(self._encode(principal_id), principal.title)

    def getValue(self, token):
        """Return the principal ID given its token."""
        return self._decode(token)


class PrincipalTerm:
    """
    A principal term.

    We have a ``token`` based on the encoded principal ID, and a ``title``.
    """

    def __init__(self, token, title):
        self.token = token
        self.title = title
