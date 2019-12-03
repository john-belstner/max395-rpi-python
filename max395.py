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

# Check for three arguements
if (len(sys.argv) != 2):
    print("")
    print("USAGE: python max395.py <bit>")
    print("WHERE: bit   = 0, 1, 2, 3, 4, 5, 6 or 7")
    print("")
    sys.exit(1)

# Assign the arguments to variables
bus = 0
cs = 0
bit = int(sys.argv[1])

# Figure out the new state
value = 1 << bit

# Write it to the SPI device
spi = spidev.SpiDev(bus, cs)
spi.max_speed_hz = 1200000

msg = value.to_bytes(1, 'big')
try:
    print("writing " + "{0:08b}".format(value) + " to SPI" + str(cs))
    spi.xfer2(msg)
except:
    print("An exception occurred writing to SPI" + str(cs))

time.sleep(.1)

value = 0
msg = value.to_bytes(1, 'big')
try:
    print("writing " + "{0:08b}".format(value) + " to SPI" + str(cs))
    spi.xfer2(msg)
except:
    print("An exception occurred writing to SPI" + str(cs))

sys.exit(0)
