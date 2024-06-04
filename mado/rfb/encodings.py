# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import struct
from enum import Enum

from mado.rfb import msg_types


class EncodingTypes(Enum):
    RAW = 0
    COPY_RECT = 1
    RRE = 2
    CORRE = 4
    HEXTILE = 5
    ZLIB = 6
    ZLIBHEX = 8
    TRLE = 15
    ZRLE = 16

    # Pseudo-encodings
    DESKTOP_SIZE = -223
    LAST_RECT = -224
    CURSOR = -239
    DESKTOP_NAME = -307
    XVP = -309
    CONTINUOUS_UPDATES = -313


def write(writer, supported_encodings):
    writer.write(
        struct.pack(
            "!BxH",
            msg_types.MessageTypes.SET_ENCODINGS.value,
            len(supported_encodings),
        )
    )
    for encoding in supported_encodings:
        writer.write(struct.pack("!i", encoding.value))
    writer.flush()
