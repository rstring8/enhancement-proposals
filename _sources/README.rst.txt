***************************
Nengo enhancement proposals
***************************

This repository contains proposals for enhancements
to the Nengo ecosystem,
dubbed Nengo Enhancement Proposals or NEPs [1]_.

.. [1] Inspired by Python's `PEPs <https://www.python.org/dev/peps/>`_
       and Jupyter's `JEPs <https://github.com/jupyter/enhancement-proposals>`_.

NEPs are a way to propose and discuss changes that will touch
multiple projects in the Nengo ecosystem,
or require a large change to one project.
NEPs allow Nengo developers to collaboratively
propose and evaluate ideas
before going through a lot of effort implementing them,
and without cluttering up the issue tracker
of individual projects.
They also allow us to have a rough roadmap
of upcoming changes to the Nengo ecosystem.

Making a proposal
=================

To propose a new Nengo enhancement,
make a pull request on the
`enhancement proposal repository
<https://github.com/nengo/enhancement-proposals>`_
adding a reStructuredText file [2]_
with the proposal.
Your reStructedText file should follow
the format of :doc:`the template <001-template>`
with all of the template text replaced with your proposal.

.. [2] reStructuredText is used over other markup formats
       as it can easily be included in Sphinx documentation.

Note that, in addition to prose,
there is a table of metadata at the start
of each NEP. Most of the steps below
involved updating that metadata.

Review process
==============

Each NEP goes through a series of stages.
In most cases, a pull request is used for each stage transition.
While anyone can make a proposal
and comment on it,
only Nengo maintainers can approve stage transitions.

The stages are as follows:

1. NEPs marked as **idea** are enhancements that we wish to make,
   but are not yet being worked on.

   When you first open your proposal PR, it is in the idea stage.
   In this stage, maintainers and developers will evaluate your proposal,
   suggest additional pros and cons, and propose alternative solutions.

   These discussions will take place through PR comments
   and at a weekly Nengo development meeting.
   During the meeting, developers will vote
   to determine if the proposal will be accepted or rejected.
   A summary of the discussion and a record of the vote
   will be added to the NEP after the meeting,
   and the PR will be merged.

2. NEPs marked as **in progress** are enhancements currently being worked.

   Developers can offer to implement approved ideas
   by making a PR that fills in their name as
   the proposed implementer,
   and provides an estimated completion date.
   The completion date is not a hard deadline,
   but it helps maintainers keep track
   of what is currently being worked on,
   and what has been abandoned.

   If a maintainer thinks that the developer is up to the task
   and that the completion date is reasonable,
   they will merge the PR.

3. NEPs marked as **implemented** are finalized enhancements
   with associated pull requests on Nengo repositories.

   Upon completion of the work described in the NEP,
   the implementer should update the NEP to include
   the completion date and where the work can be found
   (e.g., a new repository, one or more merged PRs on Nengo projects).
