*********************
NEP-404: Java backend
*********************

=================  ==========================================
Stage              Rejected
Rejected by        Trevor Bekolay, Chris Eliasmith,
                   Jan Gosmann, Daniel Rasmussen, Allen Wang
Rejection date     October 2, 2017
=================  ==========================================

Context
=======

Nengo 1.4 was implemented in Java.
We've progressed to Python for Nengo 2,
but Java's still a powerhouse in terms of language use,
and it does multithreading better than most other languages.
Most importantly, it's the language Android uses.
With a Java backend, we could write Nengo models
with the usual frontend code,
and have the backend spit out some Java class files
that implement that specific model,
which could easily be used in an Android application.

Proposal
========

Create a Java backend for Nengo
by co-opting the existing Nengo 1.4 codebase.

Details
=======

Like all other backends,
the Java backend would be encapsulated
in a ``Simulator`` object::

  with nengo.Network() as net:
      # Model stuff
  with nengo_java.Simulator(net) as sim:
      sim.run(1.0)

The main difficulty with the Java backend
is going to be dealing with the
Java / Python interface.
If we constrain the interaction
to be only one-way,
the interface is easy to define,
but it means that nodes have to be
significantly simplified.

Two-way interaction is possible;
we did it in Nengo 1.4 using `Jython <http://www.jython.org/>`_,
which has progressed a bit over the past few years.
There are also some new projects aiming to do
two-way Java / Python interop,
most notably `PyJNIus <https://github.com/kivy/pyjnius>`_.

The first step in the implementation will be
evaluating these interop methods
and making some quick prototypes.
Once an interop method has been chosen,
the existing Nengo 1.4 simulator code
should be used;
the ``Simulator`` class would essentially be
a wrapper around the core Nengo 1.4 simulator code.

Note that at one point I filtered the Nengo 1.4 history
to include only the simulator files.
It's available as
`tbekolay/nengo_java <https://github.com/tbekolay/nengo_java>`_
for whoever wants to implement this backend.

Pros and cons
=============

Reasons to implement this backend:

* Enables Nengo models running on Android phones.
* Less effort than other backends due to existing Nengo 1.4 codebase.

Reasons not to implement this backend:

* Java / Python interop is difficult, and none of the options are perfect.
  `Yak shaving <http://sethgodin.typepad.com/seths_blog/2005/03/dont_shave_that.html>`_
  is inevitable.
* A Java backend would not allow arbitrary models to run on Android apps
  due to requiring Python to construct the model.

Discussion
==========

While no one is strongly opposed to the creation
of a Nengo backend that targets the
Java Virtual Machine (JVM),
the consensus is that such a backend
is a low enough priority that we
are rejecting this proposal
in order to discourage people from
spending time on it
unless they are very strongly motivated.

Java vs Kotlin vs Scala
-----------------------

One of the reasons to believe that Java Nengo backend
would be easy to implement is that Nengo 1.4
is implemented in Java.
However, if our goal is to run Nengo models with the JVM,
it is likely that a new project would not
choose the Java language,
but instead a more modern language
that targets the JVM
(e.g., Kotlin, Scala).
Starting from scratch is a big time commitment.

Nengo on mobile phones
----------------------

If the main goal of implementing a Java backend
is to target Android phones,
it's not clear that a Java backend
is the best way to do that.

For one, doing it at scale would require
some kind of Python / Java interop,
which as noted in the details above,
is not yet possible with today's tools.
An alternative would be to implement
a Java frontend as well,
but we are strongly motivated to avoid multiple frontends.

Second, a Java backend would,
at best, only target all Android devices.
Android makes up the majority
of the mobile phone market,
but any respectable application
should have Android and IOS versions.

Finally, at the moment it is unclear
the size of model that could fit on a phone,
and how quickly the model would simulate.

All of these factors lead to a general consensus
that it would be better to get Nengo running on phones
using a client / server architecture,
as is already done with Nengo GUI.
In the simplest case, a phone can access
the Nengo GUI web interface.
For something fancier, we can implement
native GUIs for Android and IOS that
communicate with the same Nengo GUI server.

Finality
--------

This rejection is a soft rejection,
in that we highly discourage people
who are interested in Nengo from
implementing a Java backend.
However, that rejection is based on
the assumption that the Java backend
is primarily useful for targeting Android phones.
If someone is interested in developing
a Java backend for a different use case,
please start a discussion on
`the Nengo forum <https://forum.nengo.ai/>`_
describing your use case.
