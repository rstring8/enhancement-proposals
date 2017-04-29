*************************************
NEP-001: Network and model transforms
*************************************

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

There are several existing and proposed features
that do some kind of global enhancement of
either a network or built model.

For networks, features include:

- `Changing default intercepts to CosineSimilarity(d+2)
  <https://github.com/nengo/enhancement_proposals/pull/10>`_
- `SPA opt <https://github.com/nengo/nengo_spa/pull/4>`_
- `nengolib's biased connections for better decoding
  <https://github.com/arvoelke/nengolib/blob/master/doc/notebooks/examples/connection.ipynb>`_
- `The Parisien transform <https://github.com/nengo/nengo/issues/921>`_
- `Automatically determining number of neurons given approximated functions
  <https://github.com/nengo/nengo/issues/869>`_
- `Removing passthrough nodes
  <https://github.com/nengo/nengo/blob/master/nengo/utils/builder.py#L180>`_.

For models, the main existing feature is `the optimizer
<https://github.com/nengo/nengo/blob/master/nengo/builder/optimizer.py>`_,
but it is possible that parts of the existing builder code,
or features currently referenced in the
`builder refactoring PR <https://github.com/nengo/nengo/pull/1189>`_,
could be implemented as global enhancements of a built model.

This seems like a sufficient number of use cases
to introduce a new abstraction in the Nengo API
to standardize how Nengo interacts with these algorithms.

Proposal
========

I propose that all algorithms that operate globally
on a network or model conform to the same interface.
Specifically, all such algorithms should be
implemented as a callable
that can be called with a single argument,
which is the network or model instance.

Details
=======

We will refer to these algorithms as
network transforms and model transforms.
They are so named because they
accept as an argument a network or model,
and transform it (i.e., modify it in-place).

While the name will be useful for organizing
these algorithms,
there is no need for an additional abstraction
with that name in the Nengo API.
These transforms will be implemented
using the usual tools that Python provides for us.
Nengo (or, if desired, the user) will
call these callables in the usual Python way,
allowing the algorithms to be implemented
in the way most natural for the complexity of the transform.

Being normal callables, a key aspect of these transforms
is that they can be called in user models
to explicitly transform networks or models,
or they can be called automatically by Nengo
as part of the build process.

Examples
--------

A simple transform,
like the transform to bias all connections,
could be implemented as a function::

  def bias_connections(network, bias_mag=1.0):
      for conn in network.all_connections:
          if isinstance(conn.pre, nengo.Ensemble):
              conn.solver = BiasedSolver(conn.solver, magnitude=bias_mag)
              nengo.Connection(bias_node, conn.post,
                               function=solver.bias_function(conn.post.size_in),
                               synapse=None)

In this case, there is one argument
that can be optionally provided.
If the function is being called automatically by Nengo,
then it will always be set to its default value.
This makes sense for an option that should remain the same
in 99% of use cases,
but in specific instances should be modifiable
(in which case it would be called explicitly
in the user's model).

A more complicated transform
that is difficult to organize as a single function,
or has many arguments that we expect will be modified often,
can instead be implemented as a callable class::

  class OpMergeOptimizer(object):
      def __init__(self, max_iterations=1000):
          self.max_iterations = max_iterations)

      def __call__(self, model):
          # Optimize for, at most, max_iterations iterations
          ...

The callable class
will be instantiated and available
to Nengo models.
A user could therefore modify the arguments
by accessing that instance and modifying it
(through an API to be determined later;
see the next section).

Role in the Nengo 3.0 builder
-----------------------------

Nengo 3.0 will include a documented backend API,
including a refactored version of the current builder.
Currently, the builder follows a form of plugin architecture
in that the build functions associated with Nengo objects
are added at runtime, and can be modified by model code.

These network and models transforms would become
another pluggable part of the build process.
Specifically, networks transforms would be
executed before the network is built,
and model transforms would be executed
after the network is built.

Like other parts of the Nengo API,
we could include the most broadly applicable transforms
in Nengo core, and allow other packages
(like nengo_extras, nengolib, and nengo_spa)
to provide more specialized transforms.
This, however, opens the door to other packages
adding default transforms on import,
which walks a thin line between
convenient and magical.

Pros and cons
=============

The overall idea of the proposal seems
a necessary addition to Nengo 3.0,
and standardizes something that has already become
a common practice.

The details, however, should be discussed
before any implementation takes place.
The implementation described above has several benefits:

* Uses normal Python primitives,
  eliminating the need for a new abstraction in the Nengo API.
* Can be called in user models explicitly,
  or behind-the-scenes by Nengo.

But suffers from several issues:

* A transform might end up being called twice
  (once by the user, once by Nengo).
* It may not be obvious what transforms
  end up being called on a network.
* The network may change by virtue of it being built.

Discussion
==========

The name
--------

The names "network transform" and "model transform" are not great.
In particular, we already use "transform" in the API
to refer to the linear mapping from inputs to outputs
in the ``Connection`` object.
We should brainstorm alternate names.

Adding an abstraction
---------------------

The proposal above does not need an additional abstraction
because it will accept normal Python callables,
resulting in the pros and cons listed above.

We could instead introduce abstractions
for these algorithms. They would look something like::

  class NetworkTransform(object):
      def __call__(self, network):
          raise NotImplementedError("Subclasses must implement this.")

Generally, introducing this abstraction makes things
easier for us, as Nengo developers,
but harder for users.

For us, it means that we can add things to the
``NetworkTransform`` base class to track
what transforms are called on what networks.
This would allow us to:

1. Do provenance tracking of what transforms
   have been called on a given network.
2. Ensure that the same transform is not called multiple times
   on the same network.

For the user, it means that
they have to learn another abstraction in our API.
The more abstractions, the more the cognitive load,
and the harder it is to learn.
I think the idea behind these transforms is that
they should provide uncontroversial benefits,
so the user should not need to know about them
in the general case.
However, for some models, they may need
additional transforms, or to disable the default ones,
so it must be modifiable by the user.
I am unsure whether adding this abstraction
makes it easier or harder for the average user
to do what they need to do.

In terms of code style,
it could be argued that adding an explicit abstraction
means that there is only one way do things
(which follows the zen of Python).
However, this is not strictly true because
adding this abstraction does not limit
the user from transforming the network
using normal Python tools without Nengo knowing.
It could instead be argued that we
are adding one more way to do the same thing,
and that additional way is not obvious
without looking through documentation.

Should we modify in-place?
--------------------------

As described above, the transform modifies
the network and model in place.
This follows what the majority of
implemented transform do,
and in general makes sense
when the transform is called
explicitly by the user in a model::

  remove_passthrough_nodes(network)

However, were this to happen automatically in the build process,
we could run into unexpected situations::

  with nengo.Simulator(network) as sim:
      sim.run(0.1)
  sim.data[passthrough_node]  # KeyError: the node no longer exists!

There is likely no general solution to this;
we should be conservative in the transforms that we enable
by default because they can result in bugs
that will be difficult to track down.
However, we can improve the situation somewhat
by forcing all transforms to
return modified networks and models,
rather than modifying them in place.

The main benefit of returning a modified network is,
as stated, fewer bugs in user models.
In general, it should be easier to debug
transforms that return new networks,
because you can look at the network before and after
transformation to see what has changed.

However, returning a new network
would make several parts of the builder
more difficult to implement under the hood.
In particular, we expect that users
have handles to the objects in the network
and use them to access probed data.
If we make copies of the network under the hood,
then we also need to keep track
of a mapping between the old objects
and the new,
which may result in even more obscure bugs.
It also requires more physical memory,
which may not be available
for very large models.
