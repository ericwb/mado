# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import struct


EXCLUSIVE = 0x00
SHARED = 0x01


def write(writer, exclusive=True):
    writer.write(struct.pack("!B", EXCLUSIVE if exclusive else SHARED))
    writer.flush()
