**********************************
NEP-101: Convolutional connections
**********************************

=================  ==================================
Stage              Idea
Proposed by        Daniel Rasmussen <daniel.rasmussen@appliedbrainresearch.com>
Approved by
Approved on
Estimated effort   4 weeks
Implemented by
Completion date
Implemented in
=================  ==================================

Developed in consultation with:
Eric Hunsberger <eric.hunsberger@appliedbrainresearch.com>
Trevor Bekolay <trevor.bekolay@appliedbrainresearch.com>

Context
=======

Right now Nengo's Connection system is based on the assumption of dense
(all-to-all) connectivity between objects (Ensembles/Nodes).
We want to generalize this to support other connectivity patterns,
e.g. sparse/convolutional weights.
Non-dense connectivity patterns are quite common in neural network
research/applications, so it would be good to have a way to represent them with
a consistent interface across the Nengo ecosystem.

Proposal
========

The proposal is that we add a new type of object that can be passed as the
``transform`` argument on a ``Connection``, which would represent a
convolutional transformation.  E.g.::

  nengo.Connection(a.neurons, b.neurons,
                   transform=nengo.Conv2D(kernel_size=(3, 3), stride=(1, 1))

In this proposal we will focus on the specific case of convolutional
connectivity (although with the general view that this
approach should be extendable to other, related use cases in the future).
In addition, we only propose to support these transform types on
connections where the pre object is a Node or Neuron object (i.e., not an
Ensemble, meaning decoded connection).
These connections also will not support online learning rules.
See "open questions/extensions" below for more discussion on these
restrictions.

Details
=======

Some of the other options considered were creating a new connection object,
e.g.::

  nengo.Conv2DConnection(a.neurons, b.neurons, kernel_size=(3, 3),
                         stride=(1, 1))

or a ``Network`` that would encapsulate lower level objects implementing
the convolutional connection, e.g.::

  conv = nengo.networks.Conv2D(
      a.neurons, b.neurons, kernel_size=(3, 3), stride=(1, 1))

The ``transform``-based approach seemed the best option, as it adds minimal
complexity to the Nengo interface, avoids duplicating connection
logic, and scales well to other connectivity types (e.g.
``transform=nengo.Sparse(...)``).
It is also worth noting that it is conceptually similar to the idea of passing
a ``Distribution`` for the transform, which we are already introducing to
users.

Note that because we are only modifying the Connection, and not the Ensemble
parameters, every convolutional neuron will have its own gain and bias.
This is somewhat unusual, as typically those parameters would be shared within
each channel.
However, there is nothing inherently wrong with untieing these parameters
(it is not uncommonly done), and if this distinction is important to a user
they can achieve the tied effect by manually setting the gains/biases
appropriately on the post Ensemble.
We could perhaps provide a helper function to do this, if it becomes an issue.

In terms of implementation TODOs, this is actually fairly easy to implement
on the frontend side.
It is essentially the addition of a new book-keeping object, with which we'd
want to include some validation.
But other than that, the addition of this new object shouldn't affect
anything else on the frontend.

Most of the effort will be on the backend.
The reference builder would add a new operation (e.g. ``Conv2DInc``).
The reference backend can implement this operation by expanding
it to a dense weight matrix and then proceeding as normal with a ``DotInc``.
We could make this fallback approach available for any backend that does not
want to add a custom convolution implementation.
We could perhaps add a more efficient implementation as well (e.g.,
if the user has ``scipy`` installed we could use ``scipy.signal.convolve2d``).

Most of the benefit will be for other backends that have specialized
operations for convolution (e.g. NengoDL, NengoOCL, Nengo Loihi).
These will be able to provide custom implementations for ``Conv2DInc`` (if
they use the reference builder), or can treat the ``transform=nengo.Conv2D``
object however they like if they are writing their own ``Connection`` builder.
The implementation in these backends should proceed concurrently with this
proposal, to be sure that the design here meets their needs.

Open questions/extensions
-------------------------

**Passing these transform objects for other parameters**

In the same way that we can pass Distributions for transforms or encoders,
it seems natural to think about using these new objects for encoders as well
(e.g., creating convolutional encoders).
There doesn't seem to be anything particularly problematic about this, it would
just be a matter of trying it out.

**Using these objects on decoded connections**

A little more tricky is how these objects should interact with decoders.
Currently we combine the decoders and the transform on decoded connections into
a single dense weight matrix.
It wouldn't be possible to do that combination with a convolutional transform
(short of expanding the convolutional weights into a dense weight matrix).
One option would be to keep them distinct just in this special case.
In this case we would have a somewhat significant qualitative change in the
model when changing the transform type.
Alternatively, we could separate the decoders and transform in all cases.
This would affect online learning rules, as they would target one or the other
rather than both (as they do now).
This may also be less efficient for backends to implement, without additional
optimization on their part.

My inclination would be to leave the current behaviour unchanged and only
separate the decoders/transform for convolutional transforms.
But this issue seems more uncertain, and a resolution is not required in order
to support the vast majority of convolutional use cases (which are based
on neuron-to-neuron connections).
That is why we have excluded this issue from this proposal.

**Using these objects with online learning rules**

Similarly, it is not obvious how convolutional weights should be
affected by online learning rules (e.g., PES).
There may be some generalization of the PES update that makes sense to apply to
convolutional kernels?
At a guess, it would be something like computing the error and then aggregating
across channels.
However, again this seems like a separable issue; supporting convolutional
connections but not allowing them to be modulated by online learning rules
should cover the vast majority of convolutional network use cases, while we
explore possible applications of online learning in the future.

**Other transform types**

A ``Sparse`` transform type seems like a natural addition (allowing backends
to implement sparse matrix multiplication).
We could also do ``Conv1D``, ``Conv3D``, etc. (or perhaps those should be
combined in a single, general convolution object?).
We could also implement more specialized connectivity types, like ``Gabor``
(this would be like ``Sparse`` with a special connectivity
pattern/initialization).
We limit this proposal to convolutional connectivity, but we should keep
these other patterns in mind to make sure that the approach we adopt here will
generalize.

Pros and cons
=============

Pros:

* Provides a consistent way to define convolutional connections across backends
* Minimal disruption to existing frontend interface
* Easy for backends to insert custom implementations

Cons:

* Nonzero addition to frontend complexity (another thing for users to
  learn/think about)
* Adds additional complexity to the connection build process
* Does not address some potentially important issues (e.g. interaction with
  NEF decoding and online learning)
* Somewhat more complicated to implement tied gains/biases


Discussion
==========

* Do we want to add frontend support for convolution?
* If so, is the transform-based approach the best one?
* Do we want to include any of the open questions/extensions in this proposal?

One section per discussion point
--------------------------------

Each discussion point will be discussed
at a developer meeting.

After the meeting,
update the proposal with a summary
of the discussion for each point.
