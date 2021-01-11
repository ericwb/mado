# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import struct

from mado.rfb import msg_types


def write(writer, button_mask, x, y):
    writer.write(struct.pack(
        '!BBHH',
        msg_types.MessageTypes.POINTER_EVENT.value,
        button_mask,
        x,
        y
    ))
    writer.flush()
