####################################
NeoTrellis setup and troubleshooting
####################################

The Neotrellis connects to the RPi over ``i2c`` bus #1 (GPIO pins 3 and 5).

Testing that the neotrellis is connected can be done from the shell with
``i2cdetect -y 1``, which should return the address of the neotrellis (0x2E)
at the end of the address block.
If it does not detect anything (all ``--`` throughout the block), then it means
that the neotrellis is not connected properly.

If you do not see an i2c connection, unplug and replug the GPIO pins going
to the trellis, and check intermediate connections. This is typically the
issue.
