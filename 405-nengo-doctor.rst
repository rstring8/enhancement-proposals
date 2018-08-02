**************************
NEP-001: Proposal template
**************************

=================  ==================================
Stage              Idea 
Proposed by        Chris Eliasmith <chris@abr.rocks>
Approved by
Approved on
Estimated effort
Implemented by
Completion date
Implemented in
=================  ==================================

Context
=======

This is an idea from Aaron Voelker for improving the experience of new
and experienced users when optimizing/tuning their models.  Right now it's
easy to make many suboptimal designs, which are hard to debug.  This EAP
is regarding 'Nengo Doctor' (NengoDR) which would be a kind of neural
profiler that could help catch errors or likely issues with a model.

Proposal
========

The idea is to have a special 'simulator' that would run the model and analyze
it in real time, producing a report at the end that highlights potential
issues or optimizations.  You could imagine many sorts of things to monitor: are there
many neurons that never spike? Do a large number of neurons saturate? Are the
decoder values within some range? A big part of specifying and fleshing out the 
EAP are determining a starting set of questions that are answered by this
'optimizing' simulator.  You could imagine different levels of detail/warnings
depending on how important the issue is for model simulation.

Details
=======

In addition to the basic idea above, it might be possible to try 
certain optimizations automatically on different versions
of the same model and tell the user what
effects it has (e.g. picking certain kinds of optimizers, playing with particular
optimizer parameters, etc.).  Essentially it would be a tester or profiler that
could guide users to build better models (under many possible interpretations
of 'better').

You could imagine trying different filters, and showing effects.  The possibilities
are endless :)

It might also make sense, if this works well, to have a similar kind of thing for
different backends. So the suggestions/optimizations could be backend specific.

You can make additional sections
--------------------------------

Which can include source code::

  "like this!"

And references to `external resources <https://github.com/nengo/>`_.

Pros and cons
=============

Pros:

* Would help many users build better models
* Could systematize a lot of deep knowledge we have about how to
build good models and make it more accessible to other users
* Great for debugging models, enhances Nengo's usability

Cons:

* Is a lot of work
* It's usefulness would be determined by lots of complicated design decisions,
but such is software development
* It's pretty under-specified at this point

These lists help maintainers evaluate the proposal.
Maintainers may add to these lists during the review process.

Discussion
==========

List discussion points about the detailed description.
This can include salient alternatives to the proposal,
or anything else that you think should be discussed.

One section per discussion point
--------------------------------

Each discussion point will be discussed
at a developer meeting.

After the meeting,
update the proposal with a summary
of the discussion for each point.
