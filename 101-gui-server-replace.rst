*******************************
NEP-101: GUI server replacement
*******************************

=================  =====================================
Stage              Idea
Proposed by        Trevor Bekolay <tbekolay@gmail.com>
Approved by
Approved on
Estimated effort   3 weeks
Implemented by
Completion date
Implemented in
=================  =====================================

Context
=======

The Nengo GUI contains its own HTTP server,
which subclasses the Python standard library's
`http.server <https://docs.python.org/3/library/http.server.html>`_.
It's generally accepted that the standard library's server
is a development server, not a production quality server,
meaning that it will not scale up to handling
many simultaneous requests.

It could be argued that because the server
is typically only running on your local machine,
it does not have to handle many requests.
However, even in this context it is helpful
to have a robust HTTP server.
As evidence, similar tools as the Nengo GUI
(`the Jupyter notebook
<http://jupyter-notebook.readthedocs.io/en/stable/public_server.html>`_
and `Bokeh <https://github.com/bokeh/bokeh/issues/1218>`_)
use Tornado instead of rolling their own server infrastructure.

It could also be argued that keeping control
over the server infrastructure means that
we are better able to fix bugs and inefficiencies.
However, many of the Nengo GUI bugs filed
have been related to the server.
Since we subclass from
the Python standard library HTTP server,
it is essentially impossible to be very efficient.
Generally, web technologies are complex and rapidly changing.
Nengo developers should be focused on developing Nengo,
not keeping up with web technologies
and optimizing HTTP servers.

Finally, it could be argued that switching servers
will increase our development burden
due to needing to learn someone else's API
rather than developing the API that best suits Nengo GUI.
Anecdotally, I can say that the server code
is currently difficult to work with,
in part because the standard library's API
must be extended with subclasess,
which is generally difficult to use.
Somewhat more objectively,
there was a very old PR that included
`migrating to Tornado <https://github.com/ctn-archive/nengo_gui_2014/pull/1/commits/695b28dc4b77af4d52b7ecdccbb14fa632bc0a0e>`_,
which ended up removing 324 lines of code,
suggesting that code will end up shorter
and simpler if we migrate.

Proposal
========

I propose we replace the current server code
that subclasses ``http.server`` and related classes
with a robust third-party Python HTTP server.

Details
=======

There are several choices
for robust Python HTTP servers.
The first step in this project would be
to evaluate a number of servers
and choose the best one.
The list of servers to evaluate should include, at least

* `Tornado <http://www.tornadoweb.org/en/stable/>`_
* `Twisted <https://twistedmatrix.com/trac/>`_
* `uWSGI <http://uwsgi-docs.readthedocs.io/en/latest/index.html>`_
* `gunicorn <http://gunicorn.org/>`_

Note that some of those servers are WSGI servers,
which could be used as is or with
a WSGI framework like `Flask <http://flask.pocoo.org/>`_
or `Falcon <https://falconframework.org/>`_.

Pros and cons
=============

* Simpler, more readable Nengo GUI code.
* More robust and scalable Nengo GUI,
  could be easily used in a cloud hosting paradigm.
* Far more likely to stay up-to-date with modern web technologies.

The only con that I am aware of is:

* Introduces at least one dependency which may be difficult to install,
  especially in offline contexts.

It should, however, be noted that the Python packaging ecosystem
has advanced significantly since
the PR involving Tornado was made in 2014.
Specifically, ``wheels`` and ``conda`` make it
possible to save compiled binaries to a USB stick
and install them without requiring internet access.
I would hazard a guess that it would take less long-term effort
to make a script that puts all the wheels needed
for an offline Nengo GUI install on a USB stick
than to fix some of the bugs
that currently exist in our server.

Discussion
==========
