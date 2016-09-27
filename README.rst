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
make a pull request on this repository
adding a reStructuredText file [2]_
with the proposal.
Your reStructedText file should follow
the format of ``000-template.rst`` with
all of the template text replaced with your proposal.

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

   Once discussion settles down, a maintainer will choose to either
   reject the proposal by closing the PR unmerged,
   or will approve it by merging the PR.

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

   The PR should update the completion date and
   point to the merged PRs.

Note that the PRs coming out of these proposals
go through normal review processes,
and as a result could be rejected
even if the proposal was accepted.
In these cases, the proposal will be
reverted from **in progress** to **idea**.
