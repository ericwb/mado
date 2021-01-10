# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.rfb import unsigned8


class ClientInitMsg():
    EXCLUSIVE = 0x00
    SHARED = 0x01

    def __init__(self):
        self.shared = self.EXCLUSIVE

    def write(self, writer):
        unsigned8.write(writer, self.shared)
