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
"""Authentication interfaces
"""
from zope.interface import Interface
from zope.schema.interfaces import ISource
from zope.security.interfaces import IGroup
from zope.security.interfaces import IPrincipal


class PrincipalLookupError(LookupError):
    """No principal for given principal id"""


class IUnauthenticatedPrincipal(IPrincipal):
    """A principal that hasn't been authenticated.

    Authenticated principals are preferable to UnauthenticatedPrincipals.
    """


class IFallbackUnauthenticatedPrincipal(IUnauthenticatedPrincipal):
    """Marker interface for the fallback unauthenticated principal.

    This principal can be used by publications to set on a request if
    no principal, not even an unauthenticated principal, was returned
    by any authentication utility to fulfil the contract of
    IApplicationRequest.
    """


class IUnauthenticatedGroup(IGroup):
    """A group containing unauthenticated users"""


class IAuthenticatedGroup(IGroup):
    """A group containing authenticated users"""


class IEveryoneGroup(IGroup):
    """A group containing all users"""


class IAuthentication(Interface):
    """Provide support for establishing principals for requests.

    This is implemented by performing protocol-specific actions, such as
    issuing challenges or providing login interfaces.

    :class:`IAuthentication` objects are used to implement authentication
    utilities. Because they implement utilities, they are expected to
    collaborate with utilities in other contexts. Client code doesn't search a
    context and call multiple utilities. Instead, client code will call the
    most specific utility in a place and rely on the utility to delegate to
    other utilities as necessary.

    The interface doesn't include methods for data management. Utilities may
    use external data and not allow management in Zope. Simularly, the data to
    be managed may vary with different implementations of a utility.
    """

    def authenticate(request):
        """Identify a principal for a request.

        If a principal can be identified, then return the
        principal. Otherwise, return None.

        The request object is fairly opaque. We may decide
        that it implements some generic request interface.

        .. note::

           Implementation note: It is likely that the component will dispatch
           to another component based on the actual
           request interface. This will allow different
           kinds of requests to be handled correctly.

           For example, a component that authenticates
           based on user names and passwords might request
           an adapter for the request as in::

              getpw = getAdapter(request, context=self)

           The ``context`` keyword argument is used to control
           where the :class:`ILoginPassword` component is searched for.
           This is necessary because requests are placeless.
        """

    def unauthenticatedPrincipal():
        """Return the unauthenticated principal, if one is defined.

        Return None if no unauthenticated principal is defined.

        The unauthenticated principal must provide
        :class:`IUnauthenticatedPrincipal`.
        """

    def unauthorized(id, request):
        """Signal an authorization failure.

        This method is called when an auhorization problem
        occurs. It can perform a variety of actions, such
        as issuing an HTTP authentication challenge or
        displaying a login interface.

        Note that the authentication utility nearest to the
        requested resource is called. It is up to
        authentication utility implementations to
        collaborate with utilities higher in the object
        hierarchy.

        If no principal has been identified, id will be
        None.
        """

    def getPrincipal(id):
        """Get principal meta-data.

        Returns an object of type :class:`~.IPrincipal` for the given principal
        id. A :class:`PrincipalLookupError` is raised if the principal cannot
        be found.

        Note that the authentication utility nearest to the requested
        resource is called. It is up to authentication utility
        implementations to collaborate with utilities higher in the
        object hierarchy.
        """


class ILoginPassword(Interface):
    """A password based login.

    An :class:`IAuthentication` utility may use this (adapting a request),
    to discover the login/password passed from the user, or to
    indicate that a login is required.
    """

    def getLogin():
        """Return login name, or None if no login name found."""

    def getPassword():
        """Return password, or None if no login name found.

        If there's a login but no password, return empty string.
        """

    def needLogin(realm):
        """Indicate that a login is needed.

        The realm argument is the name of the principal registry.
        """


class IPrincipalSource(ISource):
    """A Source of Principal Ids"""


class ILogout(Interface):
    """Provides support for logging out."""

    def logout(request):
        """Perform a logout."""


class ILogoutSupported(Interface):
    """A marker indicating that the security configuration supports logout.

    Provide an adapter to this interface to signal that the security system
    supports logout.
    """
