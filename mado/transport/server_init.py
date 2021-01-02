# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import ascii_str
from mado.transport import pixel_format
from mado.transport import unsigned16


class ServerInitMsg():

    def __init__(self, reader):
        self.read(reader)

    def read(self, reader):
        self.fb_width = unsigned16.read(reader)
        self.fb_height = unsigned16.read(reader)
        self.pix_format = pixel_format.PixelFormat(reader)
        self.name = ascii_str.read(reader)

    def __repr__(self):
        return 'ServerInitMsg: %s' % vars(self)

    def __str__(self):
        return 'ServerInitMsg: %s' % vars(self)
