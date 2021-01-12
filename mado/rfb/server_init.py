# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import errno
import os
import struct

from mado.rfb import ascii_str
from mado.rfb import pixel_format


# +--------------+--------------+------------------------------+
# | No. of bytes | Type [Value] | Description                  |
# +--------------+--------------+------------------------------+
# | 2            | U16          | framebuffer-width in pixels  |
# | 2            | U16          | framebuffer-height in pixels |
# | 16           | PIXEL_FORMAT | server-pixel-format          |
# | 4            | U32          | name-length                  |
# | name-length  | U8 array     | name-string                  |
# +--------------+--------------+------------------------------+
FORMAT = '!HH'


class ServerInitMsg():

    def __init__(self, reader):
        self.read(reader)

    def read(self, reader):
        byte_array = bytearray(struct.calcsize(FORMAT))
        bytes_read = reader.readinto(byte_array)
        if bytes_read <= 0:
            raise BrokenPipeError(errno.EPIPE, os.strerror(errno.EPIPE))

        (self.fb_width, self.fb_height) = struct.unpack(FORMAT, byte_array)
        self.pix_format = pixel_format.PixelFormat(reader)
        self.name = ascii_str.read(reader)

    def __repr__(self):
        return 'ServerInitMsg: %s' % vars(self)

    def __str__(self):
        return 'ServerInitMsg: %s' % vars(self)
