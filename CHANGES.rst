=========
 Changes
=========

6.0 (2025-09-12)
================

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.


5.1 (2025-02-13)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7, 3.8.


5.0 (2023-01-06)
================

- Add support for Python 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.


4.5.0 (2021-03-19)
==================

- Add support for Python 3.8 and 3.9.

- Drop support for Python 3.4.

- Fix deprecated test imports from zope.component to use the correct
  imports from zope.interface.

4.4.0 (2018-08-24)
==================

- Host documentation at https://zopeauthentication.readthedocs.io

- Add support for Python 3.7.

- Drop support for Python 3.3.

- Drop support for ``python setup.py test``.


4.3.0 (2017-05-11)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.2.


4.2.1 (2015-06-05)
==================

- Add support for PyPy3 and Python 3.2.


4.2.0 (2014-12-26)
==================

- Add support for PyPy.  PyPy3 support is blocked on a release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946

- Add support for Python 3.4.

- Add support for testing on Travis.


4.1.0 (2013-02-21)
==================

- Add support for Python 3.3.

- Add ``tox.ini`` and ``MANIFEST.in``.


4.0.0 (2012-07-04)
==================

- Break inappropriate testing dependency on ``zope.component.nextutility``.

  (Forward-compatibility with ``zope.component`` 4.0.0).

- Replace deprecated ``zope.component.adapts`` usage with equivalent
  ``zope.component.adapter`` decorator.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


3.7.1 (2010-04-30)
==================

- Remove undeclared testing dependency on ``zope.testing``.

3.7.0 (2009-03-14)
==================

Initial release. This package was split off from ``zope.app.security`` to
provide a separate common interface definition for authentication utilities
without extra dependencies.
