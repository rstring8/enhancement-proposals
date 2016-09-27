************************
NEP-001: Population mode
************************

=================  ===================================
Stage              Idea
Proposed by        Trevor Bekolay <tbekolay@gmail.com>
Approved by
Implemented by
Completion date
Implemented in
=================  ===================================

Context
=======

Nengo can use several neuron types,
as well as a special type, ``nengo.Direct``.
Direct mode, as it's commonly called,
represents vectors perfectly
and transforms them through normal Python functions
rather than neural approximations.
This is faster than using neurons,
and so is nice for doing prototyping.
However, it is not possible to prototype
models that rely on certain neural effects,
notably saturation and inhibition.

Proposal
========

I propose to add a new special neuron type,
tentatively called ``nengo.Population``,
that is similar to ``nengo.Direct`` in that
it is not constrained to be neuron-like
and biologically plausible,
but is similar to other neurons types
in that it saturates and can be inhibited.

Details
=======

An approach emulating the activity
of an ensemble of LIF neurons was published
`by Bryan Tripp <http://www.mitpressjournals.org/doi/abs/10.1162/NECO_a_00734>`_,
and implemented on FPGAs
`by Murphy Berzish <http://compneuro.uwaterloo.ca/files/publications/berzish2016.pdf>`_.

Other approaches may also be possible.
The first step in pursing this idea
is to enumerate possible ways to implement population mode
and weight the pros and cons of each approach.

Pros and cons
=============

We should implement population mode because it:

* Allows prototyping of a wider range of networks than direct mode.
* Could emulate neural activity much faster than rate neurons.
* Allows simulating networks with larger timesteps,
  further speeding up the simulation.

It might be difficult because:

* There are lots of possible approaches,
  so reviewing them all will be time-consuming.
* There are lots of possible approaches,
  so it may not be easy to choose a best approach.
* Population mode will have to be implemented
  separately on any backend wanting to support population mode.
  This implementation may be more involved than
  a normal neuron type.
