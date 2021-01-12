# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import errno
import os
import struct

from mado.rfb import encodings


# +--------------+--------------+---------------+
# | No. of bytes | Type [Value] | Description   |
# +--------------+--------------+---------------+
# | 2            | U16          | x-position    |
# | 2            | U16          | y-position    |
# | 2            | U16          | width         |
# | 2            | U16          | height        |
# | 4            | S32          | encoding-type |
# +--------------+--------------+---------------+
FORMAT = '!HHHHi'


class Rectangle():

    def __init__(self, reader):
        self.read(reader)

    def read(self, reader):
        byte_array = bytearray(struct.calcsize(FORMAT))
        if reader.readinto(byte_array) <= 0:
            raise BrokenPipeError(errno.EPIPE, os.strerror(errno.EPIPE))
        (self.x, self.y, self.width, self.height, encoding) = struct.unpack(FORMAT, byte_array)
        self.encoding = encodings.EncodingTypes(encoding)

    def __repr__(self):
        return 'Rectangle: %s' % vars(self)

    def __str__(self):
        return 'Rectangle: %s' % vars(self)
