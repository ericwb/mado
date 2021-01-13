# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import struct

from mado.rfb import msg_types


def write(writer, down, button, x, y):
    #print('down:{} button:{} x:{} y:{}'.format(down, button, x, y))
    button_mask = 1 << (button - 1) if down else 0
    writer.write(struct.pack(
        '!BBHH',
        msg_types.MessageTypes.POINTER_EVENT.value,
        button_mask,
        x,
        y
    ))
    writer.flush()
