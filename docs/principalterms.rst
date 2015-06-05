Principal Terms
===============

.. testsetup::

   from zope.component.testing import setUp
   setUp()

Principal Terms are used to support browser interfaces for searching principal
sources. They provide access to tokens and titles for values. The principal
terms view uses an authentication utility to get principal titles. Let's
create an authentication utility to demonstrate how this works:

.. doctest::

   >>> class Principal(object):
   ...     def __init__(self, id, title):
   ...         self.id, self.title = id, title

   >>> from zope.interface import implementer
   >>> from zope.authentication.interfaces import IAuthentication
   >>> from zope.authentication.interfaces import PrincipalLookupError
   >>> @implementer(IAuthentication)
   ... class AuthUtility:
   ...     data = {'jim': 'Jim Fulton', 'stephan': 'Stephan Richter'}
   ...
   ...     def getPrincipal(self, id):
   ...         title = self.data.get(id)
   ...         if title is not None:
   ...             return Principal(id, title)
   ...         raise PrincipalLookupError

Now we need to install the authentication utility:

.. doctest::

   >>> from zope.component import provideUtility
   >>> provideUtility(AuthUtility(), IAuthentication)

We need a principal source so that we can create a view from it.

.. doctest::

   >>> from zope.component import getUtility
   >>> class PrincipalSource(object):
   ...     def __contains__(self, id):
   ...          auth = getUtility(IAuthentication)
   ...          try:
   ...              auth.getPrincipal(id)
   ...          except PrincipalLookupError:
   ...              return False
   ...          else:
   ...              return True

Now we can create an terms view and ask the terms view for terms:

.. doctest::

   >>> from zope.authentication.principal import PrincipalTerms
   >>> terms = PrincipalTerms(PrincipalSource(), None)
   >>> term = terms.getTerm('stephan')
   >>> term.title
   'Stephan Richter'
   >>> term.token
   u'c3RlcGhhbg__'

If we ask for a term that does not exist, we get a lookup error:

.. doctest::

   >>> terms.getTerm('bob')
   Traceback (most recent call last):
   ...
   LookupError: bob

If we have a token, we can get the principal id for it.

.. doctest::

   >>> terms.getValue('c3RlcGhhbg__')
   u'stephan'

.. testcleanup::

   from zope.component.testing import tearDown
