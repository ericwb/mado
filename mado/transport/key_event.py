# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import msg_types
from mado.transport import unsigned8
from mado.transport import unsigned16
from mado.transport import unsigned32


KEY_MAP = {
    'space': 32,
    'exclam': 33,
    'quotedbl': 34,
    'numbersign': 35,
    'dollar': 36,
    'percent': 37,
    'ampersand': 38,
    'apostrophe': 39,
    'parenleft': 40,
    'parenright': 41,
    'asterisk': 42,
    'plus': 43,
    'comma': 44,
    'minus': 45,
    'period': 46,
    'slash': 47,
    'colon': 58,
    'semicolon': 59,
    'less': 60,
    'equal': 61,
    'greater': 62,
    'question': 63,
    'at': 64,
    'bracketleft': 91,
    'backslash': 92,
    'bracketright': 93,
    'asciicircum': 94,
    'underscore': 95,
    'grave': 96,
    'braceleft': 123,
    'bar': 124,
    'braceright': 125,
    'asciitilde': 126,
    'BackSpace': 0xff08,
    'Return': 0xff0d,
    'Escape': 0xff1b,
    'Insert': 0xff63,
    'Delete': 0xffff,
    'Home': 0xff50,
    'End': 0xff57,
    'Page Up': 0xff55,
    'Page Down': 0xff56,
    'Left': 0xff51,
    'Up': 0xff52,
    'Right': 0xff53,
    'Down': 0xff54,
    'F1': 0xffbe,
    'F2': 0xffbf,
    'F3': 0xffc0,
    'F4': 0xffc1,
    'F5': 0xffc2,
    'F6': 0xffc3,
    'F7': 0xffc4,
    'F8': 0xffc5,
    'F9': 0xffc6,
    'F10': 0xffc7,
    'F11': 0xffc8,
    'F12': 0xffc9,
    'Shift_L': 0xffe1,
    'Shift_R': 0xffe2,
    'Control_L': 0xffe3,
    'Control_R': 0xffe4,
    'Meta_L': 0xffe7,
    'Meta_R': 0xffe8,
    'Alt_L': 0xffe9,
    'Alt_R': 0xffea,
    'Caps_Lock': 0x10000,
    'Tab': 0x300009,
    'Super_L': 0x800000,
}


class KeyEvent():

    def __init__(self):
        self.msg_type = msg_types.MessageTypes.KEY_EVENT

    def write(self, writer, down_flag, key):
        unsigned8.write(writer, self.msg_type.value)
        unsigned8.write(writer, 1 if down_flag else 0)
        unsigned16.write(writer, 0)
        if key in KEY_MAP:
            unsigned32.write(writer, KEY_MAP[key])
        else:
            unsigned32.write(writer, ord(key))
