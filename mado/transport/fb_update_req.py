# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import msg_types
from mado.transport import unsigned8
from mado.transport import unsigned16


class FramebufferUpdateRequestMsg():

    def __init__(self):
        self.msg_type = msg_types.MessageTypes.FRAMEBUFFER_UPDATE_REQUEST

    def write(self, writer, x, y, width, height, incremental=True):
        unsigned8.write(writer, self.msg_type.value)
        unsigned8.write(writer, 1 if incremental else 0)
        unsigned16.write(writer, x)
        unsigned16.write(writer, y)
        unsigned16.write(writer, width)
        unsigned16.write(writer, height)
