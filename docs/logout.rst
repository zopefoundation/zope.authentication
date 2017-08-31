Logout Support
==============

.. testsetup::

   from zope.component.testing import setUp
   setUp()

Logout support is defined by a simple interface
:class:`zope.authentication.interfaces.ILogout`:

.. doctest::

   >>> from zope.authentication.interfaces import ILogout

that has a single 'logout' method.

The current use of ILogout is to adapt an
:class:`zope.authentication.interfaces.IAuthentication` instance to
:class:`~.ILogout`.  To illustrate, we'll create a simple logout implementation that
adapts :class:`~.IAuthentication`:

.. doctest::

   >>> from zope.component import adapter, provideAdapter
   >>> from zope.interface import implementer
   >>> from zope.authentication.interfaces import IAuthentication
   >>> @adapter(IAuthentication)
   ... @implementer(ILogout)
   ... class SimpleLogout(object):
   ...
   ...     def __init__(self, auth):
   ...         pass
   ...
   ...     def logout(self, request):
   ...         print('User has logged out')

   >>> provideAdapter(SimpleLogout)

and something to represent an authentication utility:

.. doctest::

   >>> @implementer(IAuthentication)
   ... class Authentication(object):
   ...     pass

   >>> auth = Authentication()

To perform a logout, we adapt auth to ``ILogout`` and call 'logout':

.. doctest::

   >>> logout = ILogout(auth)
   >>> request = object()
   >>> logout.logout(request)
   User has logged out


The 'NoLogout' Adapter
----------------------

The :class:`zope.authentication.logout.NoLogout` class can be registered as
a fallback provider of ``ILogout`` for ``IAuthentication`` components that
are not otherwise adaptable to ``ILogout``.  ``NoLogout``'s logout method
is a no-op.

.. doctest::

   >>> from zope.authentication.logout import NoLogout
   >>> NoLogout(auth).logout(request)


Logout User Interface
---------------------

Because some authentication protocols do not formally support logout, it may
not be possible for a user to logout once he or she has logged in. In such
cases, it would be inappropriate to present a user interface for logging out.

Because logout support is site-configurable, Zope provides an adapter that,
when registered, indicates that the site is configured for logout.
This class merely serves as a flag as it implements ILogoutSupported:

.. doctest::

   >>> from zope.authentication.logout import LogoutSupported
   >>> from zope.authentication.interfaces import ILogoutSupported
   >>> ILogoutSupported.implementedBy(LogoutSupported)
   True
   >>> ILogoutSupported.providedBy(LogoutSupported(request))
   True

.. testcleanup::

   from zope.component.testing import tearDown
   tearDown()
