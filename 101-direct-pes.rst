***************************
NEP-101: PES in direct mode
***************************

=================  ==============================================
Stage              Idea
Proposed by        Trevor Bekolay <tbekolay@gmail.com>
Approved on        October 16, 2017
Approved by        Trevor Bekolay, Chris Eliasmith, Jan Gosmann,
                   Daniel Rasmussen, Terry Stewart, Allen Wang
Estimated effort   6 weeks
Implemented by
Completion date
Implemented in
=================  ==============================================

Context
=======

The PES learning rule allows Nengo to do
online error-driven learning
which is analogous to the
offline optimization done to solve for decoding weights.
Principle 2 of the NEF allows us to express the
PES update rule in terms of decoders or synaptic connection weights,
meaning that PES works in a variety of situations,
for any rate or spiking neuron type.

However, PES does not work in direct mode
(i.e., when ``neuron_type`` is ``nengo.Direct()``),
as there are no decoders or connection weights to modify.
Despite that, it would be nice if
the network could function the same despite
not having weights to modify.

Proposal
========

We propose to implement custom behavior
when a PES learning rule
is applied to a connection from
a direct mode ensemble.

Details
=======

The overall idea is to maintain a lookup table
of observed error vectors
at a given part of the input vector space
so that the error can be added
to the value going across the connection,
effectively canceling out that error
and computing the correct function.
In other words, instead of the connection computing
``f(x)``, it will now compute ``f(x) + g(x)``,
where ``f`` is the function specified by the user,
and ``g`` is the accumulated observed error
experienced at input ``x``.

In terms of how this will be implemented
in the reference simulator,
a direct mode ensemble
represents its current vector value
as a ``Signal``.
For each connection from a direct mode ensemble,
an operator is added that computes
the connection's function, applies the transform,
and increments a ``Signal`` belonging to
the post object.

We will create a new ``Signal``
associated with the PES learning rule object.
That signal's shape depends on
to the dimensionality of the error signal,
the dimensionality of the input signal,
and on some possibly configurable
discretization size.
For example, if the space is discretized at a resolution
of 0.01 (assuming a radius of 1),
a one-dimensional input and error space will have shape ``(1, 201)``,
a three-dimensional input and two-dimensional error space
will have shape ``(2, 201, 201, 201)``,
and so on.

Operators will be created such that
the signal above accumulates error information over time;
that signal will then be added to the
``Signal`` belonging to the post object.

Why not function approximation?
-------------------------------

The main drawback of the lookup table approach
is that it scales poorly as the dimensionality
of the input space increases.
One way around this would be to learn weights
on a set of non-neural basis functions despite
the fact that the user has specified
that they want direct mode.
While this would be a reasonable thing to do,
we favor the lookup table approach in direct mode
because non-neural basis functions
could be implemented as a neuron type,
which would allow for the PES rule to operate
on them without needing a custom implementation.
The lookup table, on the other hand,
must be done with custom logic,
which fits with how direct mode is implemented
in the reference simulator.

What about nodes?
-----------------

Nodes and direct mode ensembles are roughly equivalent.
The above proposal could also be used to
implement PES learning across connections from nodes.
However, these connections have little hope of
becoming biologically plausible,
unlike a PES rule on a direct mode ensemble
which could easily be a non-direct ensemble.

The decision of whether to allow PES learning
on connections from nodes will be made by consensus.

Pros and cons
=============

We should implement this custom behavior
for doing PES with direct mode ensembles because it:

* Enables fast prototyping of simple learning models.
* May be useful as an alternative way to
  solve certain problems where biological plausibility
  is not necessary.

Implementing PES learning in direct mode
is not worth the effort because:

* It is much less memory efficient than PES learning
  with neurons (assuming a useful discretization
  of the input space).
* It may be slower than PES learning with neurons
  for input spaces of high dimensionality,
  since the lookup table will be large.

Discussion
==========

Use case
--------

It is worth clarifying why one
would want to use the PES rule with a direct ensemble.
The typical use case is when testing out a large network
that incorporates the PES learning rule.
If one sets ``nengo.Direct`` as the default neuron type,
the network will no longer build as the PES learning rule
requires neural activities on the ``pre`` side.
Implementing PES-like learning in direct mode
would allow easier prototyping of large networks
that use learning rules.

It should be noted that this NEP was proposed
prior to the existence of the
`activate_direct_mode
<https://github.com/nengo/nengo/blob/v2.6.0/nengo/utils/network.py#L31>`_
helper function.
This function is another approach to the
use case above,
as it does not convert ensembles involved in learning rules
to direct mode.
However, it was decided that
the existence of this function does not
make this NEP invalid,
only less urgent.

Skepticism
----------

Unlike other proposals, there is skepticism as to
whether the implementation in this NEP
will actually accomplish the use case above;
specifically, it is not clear
that a lookup table in a potentially high-dimensional space
will be able to track error information
sufficiently well to operate "like PES."

It was decided that, while we are skeptical,
we would not discourage anyone
from attempting to implement this NEP,
unlike the NEPs we have rejected.
However, someone looking to implement this NEP
should think of it as a research project
that may or may not yield results,
rather than as a missing feature
that Nengo absolutely needs.
