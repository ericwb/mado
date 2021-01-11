# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import struct

from mado.rfb import msg_types


def write(writer, x, y, width, height, incremental=True):
    writer.write(struct.pack(
        '!BBHHHH',
        msg_types.MessageTypes.FRAMEBUFFER_UPDATE_REQUEST.value,
        1 if incremental else 0,
        x,
        y,
        width,
        height
    ))
    writer.flush()
