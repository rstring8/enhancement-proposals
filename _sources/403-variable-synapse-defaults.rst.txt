**********************************
NEP-403: Variable synapse defaults
**********************************

=================  ==========================================
Stage              Rejected
Rejected by        Trevor Bekolay, Chris Eliasmith,
                   Jan Gosmann, Ben Morcos, Terry Stewart,
                   Allen Wang
Rejection date     November 7, 2016
=================  ==========================================

Context
=======

When you create a connection between two objects
and do not specify a ``synapse``,
the network default is used.
If a network default is not set,
then the global default is
``nengo.Lowpass(0.005)``
(i.e., a 5 ms lowpass filter).
While this makes sense in many cases
(e.g., ensemble to ensemble connections),
it does not make sense in other cases
(e.g., node to ensemble connections).

Proposal
========

Vary the default ``synapse`` depending on the
types of ``pre`` and ``post``.
For ensemble to ensemble connections,
the current 5 ms lowpass filter default is still appropriate.
For node to ensemble connections,
a default of ``None`` (i.e., no filtering)
would make more sense.

Details
=======

While the exactly defaults for different situations
still need to be discussed,
the general implementation has some precedent.
In ``nengo.Probe``, we allow the user to specify
the decoder solver through the ``solver`` parameter.
If no solver is passed, then the it is assigned the value
``ConnectionDefault``, which is a sentinel value
that tells the builder to use whatever solver
is the default in ``nengo.Connection``.

A similar sentinel value can be used for
the ``synapse`` parameter in ``nengo.Connection``.
When the builder encounters the sentinel value,
it will assign a synapse that is appropriate
for the types of ``pre`` and ``post``.

Pros and cons
=============

Variable synapse defaults are useful because:

* Models using passthrough nodes may not realize that
  a default filter is being applied.
  Passthrough nodes should not affect the signal,
  but the signal will be affected by the filter.
* In general, filtering the output of a node
  is unexpected by most new users.

Variable synapse defaults should not be implemented because:

* It is not clear how to set the default for each situation.
  Even if we figure out good defaults,
  users will want to change it,
  as they can change the network-wide default synapse already.
* Setting a default synapse of ``None`` anywhere
  should be done with caution,
  as it can result in cycles with no filters
  (which raises an exception)
  and biologically implausible models.
* Additional cognitive load as users must remember
  the default for each case.

Discussion
==========

Ultimately the magic and additional cognitive load
is the main reason for rejection.
While it may not be intuitive for new users
that a default synapse is always applied
unless they explicitly pass ``synapse=None``,
that lesson needs to be learned eventually.
We think that it's preferable to learn that lesson
in response to too much filtering
rather than too little filtering,
which is likely to occur with variable synapse defaults.
Once the user is aware of the ``synapse`` argument
and what can be passed to it,
it's much easier to explain that the default
is ``nengo.Lowpass(0.005)`` than it is
to explain all of the possible combinations
and what the default is in each situation.
In both cases, the use is most likely to
explicitly specify the synapse in most cases
once they are aware of it.

Why 5 ms by default?
--------------------

It is worth also justifying the choice
of a default 5 ms filter.
As noted above, too much filtering
is far preferable to too little filtering.
Conceptually, Nengo objects are independent units
that communicate with each other.
That communication should take some time;
when there is no filtering,
that communication takes no time,
so the objects are no longer conceptually independent.
No filtering is not a reasonable default.

A 5 ms filter constant
is within the range of many neurotransmitters
(including GABA and AMPA receptors),
but is on the fast side.
In fact,
it is typically too fast to construct stable integrators.
We often make integrators near the end
of a novice tutorial,
which makes it an ideal time to
explain how synaptic filtering can affect dynamics.

A longer time constant would work
in the case of making integrators,
and would also work for simple feedforward networks.
There would be noticeable delays
in transferring information,
but it would eventually be transferred,
which would give users the impression that
Nengo models are slow.
Since the models still work,
users may not realize that the synaptic filter
can be changed such that some connections
occur faster than others.

To summarize: a 5 ms filter works in most cases,
but not so many cases that users rarely need to change it,
which strikes a nice balance.

Finality
--------

This rejection is unlikely to be reversed.
While we would not discourage anyone
who wants to experiment with this
for their own personal interest,
it would be nearly impossible
for that experiment
to ever wind up in Nengo.
