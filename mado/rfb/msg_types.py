# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from enum import Enum


class MessageTypes(Enum):
    FRAMEBUFFER_UPDATE = 0
    SET_COLOR_MAP_ENTRIES = 1
    BELL = 2
    SERVER_CUT_TEXT = 3

    SET_PIXEL_FORMAT = 0
    FIX_COLOR_MAP_ENTRIES = 1  # not currently supported
    SET_ENCODINGS = 2
    FRAMEBUFFER_UPDATE_REQUEST = 3
    KEY_EVENT = 4
    POINTER_EVENT = 5
    CLIENT_CUT_TEXT = 6
