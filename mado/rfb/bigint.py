# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.rfb import unsigned32


def read(reader) -> int:
    length = unsigned32.read(reader)
    return read_len(reader, length)


def read_len(reader, length: int) -> int:
    byte_array = bytearray(length)
    reader.readinto(byte_array)
    return int.from_bytes(byte_array, byteorder="big")


def write_len(writer, num: int, length: int) -> None:
    writer.write(num.to_bytes(length, byteorder="big", signed=False))
    writer.flush()
