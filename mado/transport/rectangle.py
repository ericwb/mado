# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import unsigned16


class Rectangle():

    def __init__(self, socket):
        self.read(socket)

    def read(self, socket):
        self.x = unsigned16.read(socket)
        self.y = unsigned16.read(socket)
        self.width = unsigned16.read(socket)
        self.height = unsigned16.read(socket)

    def __repr__(self):
        return 'Rectangle: %s' % vars(self)

    def __str__(self):
        return 'Rectangle: %s' % vars(self)
