# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import unsigned8
import unsigned16


class PixelFormat():

    def __init__(self, socket):
        self.read(socket)

    def read(self, socket):
        self.bits_per_pixel = unsigned8.read(socket)
        self.depth = unsigned8.read(socket)
        self.big_endian_flag = unsigned8.read(socket)
        self.true_colour_flag = unsigned8.read(socket)
        self.red_max = unsigned16.read(socket)
        self.green_max = unsigned16.read(socket)
        self.blue_max = unsigned16.read(socket)
        self.red_shift = unsigned8.read(socket)
        self.green_shift = unsigned8.read(socket)
        self.blue_shift = unsigned8.read(socket)
        self.padding = unsigned8.read(socket)

    def __repr__(self):
        return 'PixelFormat: %s' % vars(self)

    def __str__(self):
        return 'PixelFormat: %s' % vars(self)
