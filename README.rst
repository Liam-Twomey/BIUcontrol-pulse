BIUcontrol
==========

Overview
----------

This repository contains software to control the Back It Up (BIU) device, originally
developed by John Rubinstein and Yong Zi Tan at the Hospital for Sick Children. [#1]_

This is a branch of the `original BIU control software`_ , with modifications to
accomodate changed parts, new spray modes, and updated software and hardware control for new use cases.
Tested on Raspberry 3B+ and 4.

.. [#1] https://doi.org/10.1107/S2059798320012474
.. _original BIU control software: https://github.com/johnrubinstein/BIUcontrol

Modifications
-------------

- Reworked and documented code for generating GUI, activating processes, and other
  software properties.
- Added pulse spray modes to allow different sample application methods.


Usage
-----

All intended use for this code is via ``BIUgui.py``. To run it, from the command
line ``cd`` to the directory and run ``python3 BIUgui.py``. The GUI takes no
arguments, but calls the other scripts, passing parameters via CLI arguments.

The scripts can in principle be used via a different GUI, using arguments passed
to them as a rudimentary API; however, I have not tested that in the slightest.

Documentation
-------------
Docs for this software are written to work with Sphinx, and can be compiled by
running sphinx in the doc subdirectory.
