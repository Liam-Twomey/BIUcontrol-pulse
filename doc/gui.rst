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
- ``guizero`` is the graphical user interface framework [#1]_
- ``board``, ``busio``, and ``adafruit_neotrellis`` are components of
  CircuitPython, which must be installed for the NeoTrellis components to work. [#2]_
- The try-except loop for ``RPi.GPIO`` (the raspberry pi GPIO interface library) [#3]_
  and `gpio` (a dummy library from PyPI) allow the code to still be run on a PC
  for development, even though the raspberry pi libraries are only available on RPi. [#4]_

.. [#1] https://github.com/lawsie/guizero
.. [#2] https://github.com/adafruit/Adafruit_CircuitPython_NeoTrellis
.. [#3] https://pypi.org/project/RPi.GPIO
.. [#4] https://pypi.org/project/gpio

Basic information flow
======================
In the file, sections beginning with ``##`` are section titles.

GUIzero setup
-------------

- Defines the structure of the gui window on a grid.
- To find which function is executed by a button press, see the ``command`` field of the
  ``PushButton`` definiton.
- These functions are defined in ``src/BIU_gui_helper_functions.py``.

NeoTrellis Setup
----------------

- This section defines the colors for the neotrellis.
- Next, the ``pixel_button_action`` function is defined. This is called when the NeoTrellis
  updates.
- This function reacts to button presses by adjusting the light on them and calling buttons,
  which is equivalent to pressing buttons on the UI.

Final tasks
-----------

- Causes the app to actually display
- shutdown pixels and all deviced controlled through GPIO.

Helper functions
----------------
``BIU_gui_helper_functions.py`` is imported by ``BIUgui.py`` to provide functins which
interface with the other scripts which actually operate the device.
- **text_box** offers an abstraction of a paired textbox and label, for convenience
- **startprocess** initiates the continuous spray process by running ``BIUapplyandplunge.py``
  with appropriate parameters.
- **pulsestartprocess** initiates the pulsed spray process by running ``BIUapplyandplunge.py``
  with appropriate parameters.
- **powerup** provides power to the components by running ``BIUpowerupdown.py --updown up``
- **powerdown** cuts power to the components by running ``BIUpowerupdown.py --updown down``
- **cleanprocess** cleans the transducer by pulsing it in long ; assumes that a droplet of
  clean water has been placed on the back of the transducer.
