#!/usr/bin/python
#
# This script allows the RaspberryPi to talk to the
# MAXIM Serially Controlled, 8-Channel SPST Switch.
#
# The python script assumes...
# 1. There are two MAX395 chips (using CE0 and CE1).
# 2. A glass of red wine is close by at all times.
# 3. Inputs to drive these switches are from picap.
#
# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import sys
import time
import spidev
import os.path

# Check for three arguements
if (len(sys.argv) != 4):
    print("")
    print("USAGE: python max395.py <cs> <bit> <state>")
    print("WHERE: cs    = 0 or 1")
    print("       bit   = 0, 1, 2, 3, 4, 5, 6 or 7")
    print("       state = 0 or 1")
    print("")
    sys.exit(1)

# Assign the arguments to variables
cs = int(sys.argv[1])
bit = int(sys.argv[2])
state = int(sys.argv[3])

# Check if the previous state was saved
if os.path.isfile('last-state.txt'):
    file = open("last-state.txt","r")
    last_state = int(file.read(1))
    file.close()
else:
    last_state = 0

# Figure out the new state
mask = 1 << bit
value = state << bit
new_state = (last_state ^ mask) | value

# Save the new state
file = open("last-state.txt","w")
file.write(str(new_state) + "\n")
file.close()

# Write it to the SPI device
spi = spidev.SpiDev(0, cs)
spi.max_speed_hz = 1200000
msg = new_state.to_bytes(1, 'big')
try:
    print("writing " + "{0:08b}".format(new_state) + " to SPI" + str(cs))
    spi.xfer2(msg)
except:
    print("An exception occurred writing to SPI" + str(cs))

sys.exit(0)
