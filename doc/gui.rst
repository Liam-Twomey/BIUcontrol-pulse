***
GUI
***

The ``BIUgui.py`` file is the sole way a user is intended to interact with the
software. It generates a graphical user interface with the ``guizero`` library,
and translates button presses and textbox contents into execution of other script
files with specific arguments.
In this file is also the NeoTrellis interaction methods, which 

Imported libraries
==================
- ``guizero`` is the graphical user interface framework
- ``board``, ``busio``, and ``adafruit_neotrellis`` are components of
  CircuitPython, which must be installed for the NeoTrellis components to work.
- The try-except loop for ``RPi.GPIO`` (the raspberry pi GPIO interface library)
  and `gpio` (a dummy library from PyPI) allow the code to still be run on a PC
  for development, even though the raspberry pi libraries are only available on RPi.

