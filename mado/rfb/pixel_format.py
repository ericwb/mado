# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import errno
import os
import struct


# +--------------+--------------+-----------------+
# | No. of bytes | Type [Value] | Description     |
# +--------------+--------------+-----------------+
# | 1            | U8           | bits-per-pixel  |
# | 1            | U8           | depth           |
# | 1            | U8           | big-endian-flag |
# | 1            | U8           | true-color-flag |
# | 2            | U16          | red-max         |
# | 2            | U16          | green-max       |
# | 2            | U16          | blue-max        |
# | 1            | U8           | red-shift       |
# | 1            | U8           | green-shift     |
# | 1            | U8           | blue-shift      |
# | 3            |              | padding         |
# +--------------+--------------+-----------------+
FORMAT = '!BBBBHHHBBBxxx'


class PixelFormat():

    def __init__(self, reader):
        self.read(reader)

    def read(self, reader):
        byte_array = bytearray(struct.calcsize(FORMAT))
        if reader.readinto(byte_array) <= 0:
            raise BrokenPipeError(errno.EPIPE, os.strerror(errno.EPIPE))
        (self.bits_per_pixel, self.depth, self.big_endian, self.true_color,
            self.red_max, self.green_max, self.blue_max, self.red_shift,
            self.green_shift, self.blue_shift) = struct.unpack(FORMAT, byte_array)
        self.bytes_per_pixel = self.bits_per_pixel // 8

    def __repr__(self):
        return 'PixelFormat: %s' % vars(self)

    def __str__(self):
        return 'PixelFormat: %s' % vars(self)
