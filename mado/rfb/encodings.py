# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from enum import Enum

from mado.rfb import msg_types
from mado.rfb import signed32
from mado.rfb import unsigned8
from mado.rfb import unsigned16


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
    # RealVNC = 1024 to 1099
    CURSOR = -239
    DESKTOP_SIZE = -223


class SetEncodings():

    def __init__(self):
        self.msg_type = msg_types.MessageTypes.SET_ENCODINGS

    def write(self, writer, supported_encodings):
        unsigned8.write(writer, self.msg_type.value)
        unsigned8.write(writer, 0)
        unsigned16.write(writer, len(supported_encodings))
        for encoding in supported_encodings:
            signed32.write(writer, encoding.value)
