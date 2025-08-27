****************************
Overview of BIUcontrol-pulse
****************************

The Back-It-Up instrument has been adapted from the instrument made by
Yong Zi Tan and John Rubinstein. The documentation here helps explain
how this python code works to control the device, as well as some
notable pitfalls in the BIU and the choice of Python and Raspberry Pi
as the control mechanism.

Changes from the original
=========================
- Control pedal and IR sensor have been removed, as it did not interact
  correctly with the software.
- Additional options for spray hardware have been added (no significant
  changes in the code for this)
- Support for the Adafruit Neotrellis device is added, for complete control
  of the GUI from a hardware device.
