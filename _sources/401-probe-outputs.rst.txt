**********************
NEP-401: Probe outputs
**********************

=================  =====================================
Stage              Rejected
Rejected by        Trevor Bekolay, Chris Eliasmith,
                   Jan Gosmann, Daniel Rasmussen,
                   Terry Stewart, Allen Wang
Rejection date     May 8, 2017
=================  =====================================

Context
=======

``nengo.Probe`` is used in Nengo models to collect data
during the simulation.
Currently, probed data is appended to a Python list,
meaning that it is present in the memory used
by the running Python process.
If that process is halted early,
that information can be lost.
Additionally, it is not possible to get access
to that data through normal means
while the simulation is running.
For that reason, Nengo GUI does not use
the probe system, and instead inserts nodes
that are used to stream data to the browser.

Probes would be more useful if they
could provide access to probed data
different ways.

Proposal
========

Add an ``output`` parameter to ``nengo.Probe``.
The value of the ``output`` parameter determines
how the simulator will provide probed data
to other processes.

Details
=======

The ``output`` parameter should accept
an object instance that defines the desired
output format.
These objects are analogous to the
``NeuronType`` and ``LearningRuleType`` objects
in that they symbolically define
what a backend should do,
but (ideally) do not implement the logic,
as that logic would be backend specific.

All these objects should subclass from
the same class in order to make validation easier,
and to make it easier for backends to define
which output formats they support.
A ``Parameter`` subclass will also be created
to support the new output formats objects.

The superclass object should be called
``OutputFormat``,
and should contain a docstring,
a small amount of metadata
(e.g., is this a streaming output format,
is all of the history retained or only the last N timesteps, etc),
and possibly a ``__repr__`` and ``__str__`` function.
See ``nengo.LearningRuleType`` for a class with
similar requirements.

Output formats
--------------

Note that implementing this proposal does not
require implementing all of the below formats;
however, it must implement at least three
in order to show that the implementation
can scale adequately.

1. ``PythonList`` or ``NumpyArray`` or ``Memory``.
   Arguments: None.

   Probes to a Python list,
   which gets converted to a NumPy array by the simulator.
   This is the functionality that currently exists.
   It should therefore be the default value
   of the ``Probe.output`` parameter.

   Note that the conversion to a NumPy array
   may be something that we want to be supported
   by all output formats.
   Currently, the NumPy conversion happens
   in the ``ProbeDict``.
   If we are implementing alternative output formats,
   we should also implement a way to read those formats.
   It may be possible to have this be done through
   an API that the ``ProbeDict`` can call on all output formats.

2. ``Queue``.
   Arguments: maximum length.

   Probes to a Python ``deque``.
   The length of the queue is passed in as an argument,
   making this output format useful when you only want
   to know the end result of the simulation rather than
   its whole history.

3. ``UDPSocket``.
   Arguments: socket number

   Probes to a UDP socket.
   Unlike ``PythonList``, it is not guaranteed that
   a ``UDPSocket`` probe will successfully transmit all of the data.

4. ``CSVFile``.
   Arguments: file name, file name template

   Probes to a CSV file, or possibly multiple CSV files.

5. ``NeoFile``.
   Arguments: file name, file name template

   Probes to a ``NeoHDF5File``, the native datafile format for
   `Neo <https://pythonhosted.org/neo/>`_.

6. ``NPZFile`` / ``NPYFile``
   Arguments: file name, file name template

   Probes to a ``.npz`` or ``.npy`` file, which is used by NumPy.

7. ``Texture``
   Arguments: ???

   Probes to an OpenGL texture for direct rendering.

Why a new parameter and set of classes?
---------------------------------------

Adding different output formats should not affect
current models, and should be switchable
with minimal effort.
The easiest way to do that is to use
Nengo's existing config system,
which allows for setting default values.
By making a new parameter,
per-network defaults can be set.
Given that we wish to make it an object parameter,
instances make sense to describe output formats
as it follows from how we define
neuron types and learning rules.

Why not use strings to denote output formats?
---------------------------------------------

It might be possible to enumerate all the possible output formats
and pass them as strings (e.g., ``"CSVFile"``).
However, several output formats warrant
changing behavior through flags or other arguments
(e.g., the name of the CSV file).
Making classes is more clear and Pythonic
than inventing a new string format we have to parse.

Alternative naming schemes
--------------------------

By far the most contentious part of this proposal
(see the issues linked below)
is what these objects should be named.
The names above are those suggested by the proposal author,
but should be decided by consensus
before the implementation is finalized.

Alternative names that have been suggested
for the superclass:

1. ``ProbeOutput``

Alternative naming schemes for output formats
(a few examples shown, but you get the idea):

1. ``ProbePythonList``, ``ProbeCSVFile``
2. ``ToPythonList``, ``ToCSVFile`` (used as ``nengo.probe.ToPythonList`` etc)
3. ``ProbeToPythonList``, ``ProbeToCSVFile``

See also
--------

This proposal is a distillation
of the following Nengo issues and PRs:
`#207 <https://github.com/nengo/nengo/issues/207>`_,
`#613 <https://github.com/nengo/nengo/issues/613>`_,
`#654 <https://github.com/nengo/nengo/pull/654>`_.

Pros and cons
=============

Pros:

* Writing to files is pretty much necessary for analysis.
* Handling this natively in Nengo makes life much easier for modelers.

Cons:

* Users could write nodes or post-processing scripts to do this for them instead.

  * It's been over 3 years and no one's implemented it yet,
    so the alternatives must not be too difficult.

* Might be difficult for some backends to support.
* Might be a lot of non-simulation related code to maintain.

Discussion
==========

This proposal was ultimately rejected,
pending further exploration
of ways to achieve the same end goal
without having to modify the ``Probe`` object.

The most straightforward alternative to the probe output approach
is to develop a set of ``Process`` subclasses
that implement the operations
that would be done by the probe outputs.
For example, we will a ``UDPSocket`` process
that will transmit data to a UDP socket
on each timestep.
Processes are a good alternative
because we already expect users
to make ``Process`` subclasses.

Backend considerations
----------------------

One of the main concerns with probe outputs
is how backends would implement them.
There are similar concerns with ``Process`` subclasses,
but most backends are able to fall back
to running the process with Python on the CPU.
This can be very slow, but it should at least work.

When it is slow, there is precedent for implementing
``Process`` subclass-specific code in backends;
Nengo OCL implements an OpenCL kernel
for the `PresentInput process
<https://github.com/nengo/nengo_ocl/blob/fa97472c888713db2842ffcd92c13aa8ce9730ca/nengo_ocl/clra_nonlinearities.py#L1440>`_,
for example.

Therefore, compared to probe outputs,
process subclasses should be
no more difficult to implement in different backends.
In fact, they should be easier in that
backends may have ways to run
process subclasses already.

Speed considerations
--------------------

The main argument for probe outputs
is that they may have access
to more simulation internals
than a Node's output process,
and therefore probe outputs
may be significantly faster than process subclasses.

However, making changes to the API
for a hypothetical speed increase
is a prime example of premature optimization.
It was decided, instead,
to explore the process subclass first
and determine if there are significant bottlenecks
that would be alleviated
by using probe outputs instead.

Finality
--------

This rejection could be reversed
if we find that process subclasses
do have significant bottlenecks,
and there is reason to believe that
probe outputs would not suffer from the same issues.
