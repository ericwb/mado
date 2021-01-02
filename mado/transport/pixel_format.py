# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import unsigned8
from mado.transport import unsigned16


class PixelFormat():

    def __init__(self, reader):
        self.read(reader)

    def read(self, reader):
        self.bits_per_pixel = unsigned8.read(reader)
        self.depth = unsigned8.read(reader)
        self.big_endian_flag = unsigned8.read(reader)
        self.true_colour_flag = unsigned8.read(reader)
        self.red_max = unsigned16.read(reader)
        self.green_max = unsigned16.read(reader)
        self.blue_max = unsigned16.read(reader)
        self.red_shift = unsigned8.read(reader)
        self.green_shift = unsigned8.read(reader)
        self.blue_shift = unsigned8.read(reader)
        self.padding = [None] * 3

        self.padding[0] = unsigned8.read(reader)
        self.padding[1] = unsigned8.read(reader)
        self.padding[2] = unsigned8.read(reader)
        # or     CARD8 pad1;
        #        CARD16 pad2;

    def __repr__(self):
        return 'PixelFormat: %s' % vars(self)

    def __str__(self):
        return 'PixelFormat: %s' % vars(self)
