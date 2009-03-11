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
"""Permission Id Vocabulary.

This vocabulary provides permission IDs.

$Id$
"""
__docformat__ = 'restructuredtext'

import zope.component
from zope.interface import implements
from zope.schema.interfaces import ISourceQueriables
from zope.site.next import queryNextUtility

from zope.app.security.interfaces import IAuthentication
from zope.app.security.interfaces import IPrincipalSource
from zope.app.security.interfaces import PrincipalLookupError

# BBB: these vocabularies are moved to zope.security.
from zope.security.permission import PermissionsVocabulary
from zope.security.permission import PermissionIdsVocabulary


class PrincipalSource(object):
    """Generic Principal Source"""
    implements(IPrincipalSource, ISourceQueriables)

    def __contains__(self, id):
        """Test for the existence of a user.

        We want to check whether the system knows about a particular
        principal, which is referenced via its id. The source will go through
        the most local authentication utility to look for the
        principal. Whether the utility consults other utilities to give an
        answer is up to the utility itself.

        First we need to create a dummy utility that will return a user, if
        the id is 'bob'.

        >>> class DummyUtility:
        ...     def getPrincipal(self, id):
        ...         if id == 'bob':
        ...             return id
        ...         raise PrincipalLookupError(id)

        Since we do not want to bring up the entire component architecture, we
        simply monkey patch the `getUtility()` method to always return our
        dummy authentication utility.

        >>> temp = zope.component.getUtility
        >>> zope.component.getUtility = lambda iface: DummyUtility()

        Now initialize the principal source and test the method

        >>> source = PrincipalSource()
        >>> 'jim' in source
        False
        >>> 'bob' in source
        True

        Now revert our patch.

        >>> zope.component.getUtility = temp
        """
        auth = zope.component.getUtility(IAuthentication)
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

        >>> class DummyUtility1:
        ...     implements(IAuthentication)
        ...     __parent__ = None
        ...     def __repr__(self): return 'dummy1'
        >>> dummy1 = DummyUtility1()

        >>> class DummyUtility2:
        ...     implements(ISourceQueriables, IAuthentication)
        ...     __parent__ = None
        ...     def getQueriables(self):
        ...         return ('1', 1), ('2', 2), ('3', 3)
        >>> dummy2 = DummyUtility2()

        >>> class DummyUtility3(DummyUtility2):
        ...     implements(IAuthentication)
        ...     def getQueriables(self):
        ...         return ('4', 4),
        >>> dummy3 = DummyUtility3()

        >>> from zope.app.component.testing import testingNextUtility
        >>> testingNextUtility(dummy1, dummy2, IAuthentication)
        >>> testingNextUtility(dummy2, dummy3, IAuthentication)

        >>> temp = zope.component.getUtility
        >>> zope.component.getUtility = lambda iface: dummy1

        >>> source = PrincipalSource()
        >>> list(source.getQueriables())
        [(u'0', dummy1), (u'1.1', 1), (u'1.2', 2), (u'1.3', 3), (u'2.4', 4)]

        >>> zope.component.getUtility = temp
        """
        i = 0
        auth = zope.component.getUtility(IAuthentication)
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
