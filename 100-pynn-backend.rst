*********************
NEP-100: PyNN backend
*********************

=================  ===================================
Stage              Idea
Proposed by        Trevor Bekolay <tbekolay@gmail.com>
Approved on        May 1, 2017
Approved by        Trevor Bekolay, Chris Eliasmith,
                   Jan Gosmann, Terry Stewart
Estimated effort   4 weeks
Implemented by
Completion date
Implemented in
=================  ===================================

Context
=======

In the
`Nengo 2.0 paper
<http://journal.frontiersin.org/article/10.3389/fninf.2013.00048/full>`_
we make comparisons between Nengo's scripting interface
and PyNN's, since the two tools share the goal
of separating the frontend model creation code
from the simulation backend.
One of the figures compares a Nengo script
with an equivalent PyNN script.
This was done manually at the time,
but it could be automated
by writing a PyNN backend
that translates a Nengo model to
an equivalent PyNN model.

Proposal
========

Create a PyNN backend for Nengo.

Details
=======

Like all other backends,
the PyNN backend would be encapsulated
in a ``Simulator`` object::

  with nengo.Network() as net:
      # Model stuff
  with nengo_pynn.Simulator(net) as sim:
      sim.run(1.0)

Unlike other backends, some additional options
will need to be provided to the PyNN backend.
Specifically, there must be a way to specify
the PyNN backend's backend.
Likely this will be done
through keyword arguments.

Something else that would be very useful
in the PyNN backend is a method to obtain
the actually Python code that the backend
will end up executing and running.
Such a method would make it possible
to reproduce the comparisons done manually
in the Nengo paper,
and would allow more flexibility
in how the PyNN script is run.
One possible API for this is::

  with nengo_pynn.Simulator(net) as sim:
      pynn_script = sim.get_script()

Pros and cons
=============

Reasons to implement this backend:

* Enables straightforward benchmarking of Nengo versus
  other popular neural simulators.
* Enables implementing existing PyNN models in Nengo
  (with a ``PynnNode``, similar to Nengo DL's ``TensorNode``)
* Enables interfacing Nengo models with existing PyNN models.

Reasons not to implement this backend:

* Benchmarks will be criticized for being automatically generated;
  "an equivalent manually generated script would be much faster,"
  they'll say.
* PyNN-accessible backends use full weight matrices,
  so even moderately sized networks will be painfully slow.
* May allow people to continue using PyNN for longer,
  rather than facilitating a switchover to Nengo.

Discussion
==========

Stated interest
---------------

Several people (outside of the Nengo development team)
have expressed interest in such a backend.

Separate repo
-------------

The Nengo PyNN backend should be implemented
in a separate repository,
not included in the same repository
as the reference backend
or any other backend.
