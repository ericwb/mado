# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import struct

from mado.rfb import msg_types


KEY_MAP = {
    "space": 32,
    "exclam": 33,
    "quotedbl": 34,
    "numbersign": 35,
    "dollar": 36,
    "percent": 37,
    "ampersand": 38,
    "apostrophe": 39,
    "parenleft": 40,
    "parenright": 41,
    "asterisk": 42,
    "plus": 43,
    "comma": 44,
    "minus": 45,
    "period": 46,
    "slash": 47,
    "colon": 58,
    "semicolon": 59,
    "less": 60,
    "equal": 61,
    "greater": 62,
    "question": 63,
    "at": 64,
    "bracketleft": 91,
    "backslash": 92,
    "bracketright": 93,
    "asciicircum": 94,
    "underscore": 95,
    "grave": 96,
    "braceleft": 123,
    "bar": 124,
    "braceright": 125,
    "asciitilde": 126,
    "BackSpace": 0xFF08,
    "Return": 0xFF0D,
    "Escape": 0xFF1B,
    "Insert": 0xFF63,
    "Delete": 0xFFFF,
    "Home": 0xFF50,
    "End": 0xFF57,
    "Page Up": 0xFF55,
    "Page Down": 0xFF56,
    "Left": 0xFF51,
    "Up": 0xFF52,
    "Right": 0xFF53,
    "Down": 0xFF54,
    "F1": 0xFFBE,
    "F2": 0xFFBF,
    "F3": 0xFFC0,
    "F4": 0xFFC1,
    "F5": 0xFFC2,
    "F6": 0xFFC3,
    "F7": 0xFFC4,
    "F8": 0xFFC5,
    "F9": 0xFFC6,
    "F10": 0xFFC7,
    "F11": 0xFFC8,
    "F12": 0xFFC9,
    "Shift_L": 0xFFE1,
    "Shift_R": 0xFFE2,
    "Control_L": 0xFFE3,
    "Control_R": 0xFFE4,
    "Meta_L": 0xFFE7,
    "Meta_R": 0xFFE8,
    "Alt_L": 0xFFE9,
    "Alt_R": 0xFFEA,
    "Caps_Lock": 0x10000,
    "Tab": 0x300009,
    "Super_L": 0x800000,
}


def write(writer, down, key):
    writer.write(
        struct.pack(
            "!BBxxI",
            msg_types.MessageTypes.KEY_EVENT.value,
            1 if down else 0,
            KEY_MAP[key] if key in KEY_MAP else ord(key),
        )
    )
    writer.flush()
