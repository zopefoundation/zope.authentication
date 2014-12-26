Changes
=======

4.2.0 (unreleased)
------------------

- Add support for PyPy.  PyPy3 support is blocked on a release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946

- Add support for Python 3.4.

- Add support for testing on Travis.


4.1.0 (2013-02-21)
------------------

- Add support for Python 3.3.

- Add ``tox.ini`` and ``MANIFEST.in``.


4.0.0 (2012-07-04)
------------------

- Break inappropriate testing dependency on ``zope.component.nextutility``.

  (Forward-compatibility with ``zope.component`` 4.0.0).

- Replace deprecated ``zope.component.adapts`` usage with equivalent
  ``zope.component.adapter`` decorator.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


3.7.1 (2010-04-30)
------------------

- Remove undeclared testing dependency on ``zope.testing``.

3.7.0 (2009-03-14)
------------------

Initial release. This package was split off from ``zope.app.security`` to
provide a separate common interface definition for authentication utilities
without extra dependencies.
