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
#
#   Forked from zope.component.nextutility in 3.10.x.
#
from zope.interface import implementer
from zope.component.interfaces import IComponentLookup
from zope.component.interfaces import IComponents

@implementer(IComponents)
class SiteManagerStub(object):

    __bases__ = ()

    def __init__(self):
        self._utils = {}

    def setNext(self, next):
        self.__bases__ = (next, )

    def provideUtility(self, iface, util, name=''):
        self._utils[(iface, name)] = util

    def queryUtility(self, iface, name='', default=None):
        return self._utils.get((iface, name), default)

def testingNextUtility(utility, nextutility, interface, name='',
                       sitemanager=None, nextsitemanager=None):
    if sitemanager is None:
        sitemanager = SiteManagerStub()
    if nextsitemanager is None:
        nextsitemanager = SiteManagerStub()
    sitemanager.setNext(nextsitemanager)

    sitemanager.provideUtility(interface, utility, name)
    utility.__conform__ = (
        lambda iface:
        iface.isOrExtends(IComponentLookup) and sitemanager or None
        )
    nextsitemanager.provideUtility(interface, nextutility, name)
    nextutility.__conform__ = (
        lambda iface:
        iface.isOrExtends(IComponentLookup) and nextsitemanager or None
        )
