# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import msg_types
from mado.transport import unsigned8
from mado.transport import unsigned16
from mado.transport import unsigned32


class PointerEvent():

    def __init__(self):
        self.msg_type = msg_types.MessageTypes.POINTER_EVENT

    def write(self, writer, button_mask, x, y):
        unsigned8.write(writer, self.msg_type.value)
        unsigned8.write(writer, button_mask)
        unsigned16.write(writer, x)
        unsigned16.write(writer, y)
