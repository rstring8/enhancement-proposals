********************************
NEP-402: Ndarray representations
********************************

=================  ==========================================
Stage              Rejected
Rejected by        Trevor Bekolay, Chris Eliasmith,
                   Jan Gosmann, Terry Stewart, Allen Wang
Rejection date     October 24, 2016
=================  ==========================================

Context
=======

There is often a desire for Nengo
to work more like NumPy
since we make liberal use of it
in the frontend and in the reference simulator.
It's common for a node function
to have to ``ravel`` some internal representation
to expose it to Nengo,
and for some vector from Nengo needing a
``reshape`` before later use.
Under the hood, NumPy also represents ndarrays
as vectors of numbers,
so why can't Nengo do the same?

Proposal
========

Generalize ensemble and node representations
to be ndarrays instead of vectors.
This means instead of ``dimensionality``,
we have ``shape``;
instead of ``size_in`` and ``size_out``,
we have ``shape_in`` and ``shape_out``.

Details
=======

In order to minimize changes to backends,
the underlying representation of ensembles
should remain a vector.
The shape of the ensemble
(which replaces the dimensionality)
defines a view on the underlying vector.
In the ideal case, that mapping would be dealt with
in the frontend, but that is unfortunately not possible.
However, it can be dealt with in the build phase.
Helper functions for dealing with the mapping
will be developed so that other backends
don't have to reimplement that logic.

Pros and cons
=============

We should generalize to ndarray representation because:

* Makes interoperating with NumPy easier.
* Paves the way for a future API that looks more like
  traditional programming (but uses neurons under the hood).

We should stick with vector representation because:

* Transformations between arbitrary ndarrays would be
  very difficult to define.
  Might require deprecating ``transform`` and requiring
  slices, which might necessitate a new ``weight`` argument.
* Neural computation is significantly different from
  traditional programming. We should not give
  the impression that they are similar.

Discussion
==========

This would be a pretty huge change to Nengo,
requiring significant backward-incompatible
frontend changes and changes in every backend.
That might be okay if it were a clear win
that made Nengo simpler, more powerful,
faster, etc.
However, the benefit here is not that obvious,
and the two downsides mentioned above
are serious.

Slippery slope
--------------

Allowing ndarray representations is the next
step after vector representations
in the Neural Engineering book.
However, there are further steps after matrices,
names functions and vector fields.
One can image stages after that too.
Adding ndarrays implies that we would also
add function and vector field representations,
which does not seem like something Nengo core
should be doing.

Terry tried it
--------------

It's worth also noting that Terry
has experimented with some preliminary Python APIs
that included ndarray representations.
It complicated the code unnecessarily,
and he would not recommend it.

Finality
--------

This rejection is unlikely to be reversed.
While we would not discourage anyone
who wants to experiment with this
for their own personal interest,
it would be nearly impossible
for that experiment
to ever wind up in Nengo.
