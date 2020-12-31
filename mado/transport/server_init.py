# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import ascii_str
from mado.transport import pixel_format
from mado.transport import unsigned16


class ServerInitMsg():

    def __init__(self, socket):
        self.read(socket)

    def read(self, socket):
        self.fb_width = unsigned16.read(socket)
        self.fb_height = unsigned16.read(socket)
        self.pix_format = pixel_format.PixelFormat(socket)
        self.name = ascii_str.read(socket)

    def __repr__(self):
        return 'ServerInitMsg: %s' % vars(self)

    def __str__(self):
        return 'ServerInitMsg: %s' % vars(self)