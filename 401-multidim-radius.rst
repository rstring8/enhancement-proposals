********************************
NEP-401: Multidimensional radius
********************************

=================  ==========================================
Stage              Rejected
Rejected by        Trevor Bekolay <tbekolay@gmail.com>,
                   Terry Stewart <tcstewar@uwaterloo.ca>,
                   Chris Eliasmith <celiasmith@uwaterloo.ca>
Rejection date     October 17, 2016
=================  ==========================================

Context
=======

The radius of an ensemble specifies the range of values
it is expected to represent.
Setting the radius to an appropriate value
can have a large impact on the accuracy
of a network. [1]_

.. [1] See `Gosmann & Eliasmith, 2016 <http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0149928>`_
       for an example.

Under the hood, the radius has no effect on a running simulation,
it only affects the build process.
Specifically:

1. Evaluation points are scaled by the radius.
2. Encoders are divided by the radius.

Essentially, Nengo maps the input value to a radius of 1
by dividing encoders by 1,
and ensures the decoded value will be
scaled to the original radius
by scaling the evaluation points used
in the decoder solving process.

Proposal
========

Since encoders and evaluation points
are the same dimensionality as the ensemble,
we should allow the radius
to also be multidimensional,
as some ensemble represent values
where each dimension has a different natural range.

Details
=======

This change would be relatively small
in terms of the lines of code changed.
The ``Ensemble.radius`` parameter would be
changed to an ``NdarrayParam``,
possibly with some additional validation
to ensure that the radius is always positive and non-zero.
The builder would need very few changes
as the radius is only used in the two places
listed above.

Pros and cons
=============

The radius should be multidimensional because:

* Ensembles representing values of differing range
  come up in real-world models.
* It requires minimal changes to the existing code.

The radius should remain scalar because:

* It is possible to manually scale values to be
  in the same range using a transform or function.
* While the code change is minimal,
  the result of the code change may not be straightforward,
  resulting in subtle bugs.

Reasons for rejection
=====================

Multidimensional radii were introduced in Nengo 1.4
late in its lifecycle,
and did not work as intended.
Indeed, it's difficult to tell what should happen
with a multidimensional radius.
In particular, the distribution of evaluation points
makes a significant impact on the accuracy
of the network.
It is not clear whether it is valid to
sample from a uniform hypersphere
and stretch the points to a hyperellipsoid.

This rejection could be reversed
if significant analysis and testing is done
to see the effects of multidimensional radii
both theoretically and in practice.
Until that analysis is done,
the radius will remain a scalar value.
