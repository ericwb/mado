# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.rfb import unsigned16


class Rectangle():

    def __init__(self, reader):
        self.read(reader)

    def read(self, reader):
        self.x = unsigned16.read(reader)
        self.y = unsigned16.read(reader)
        self.width = unsigned16.read(reader)
        self.height = unsigned16.read(reader)

    def __repr__(self):
        return 'Rectangle: %s' % vars(self)

    def __str__(self):
        return 'Rectangle: %s' % vars(self)
