# SPDX-License-Identifier: GPL-3.0-or-later
import unsigned8


class ClientInitMsg():
    EXCLUSIVE = 0x00
    SHARED = 0x01

    def __init__(self):
        self.shared = self.EXCLUSIVE

    def write(self, socket):
        unsigned8.write(socket, self.shared)
