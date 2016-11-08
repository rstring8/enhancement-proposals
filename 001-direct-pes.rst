***************************
NEP-001: PES in direct mode
***************************

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
