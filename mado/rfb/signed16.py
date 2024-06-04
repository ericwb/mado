# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import errno
import os


SIZE = 2


def read(reader):
    byte_array = bytearray(SIZE)
    return readinto(reader, byte_array)


def readinto(reader, byte_array):
    if reader.readinto(byte_array) <= 0:
        raise BrokenPipeError(errno.EPIPE, os.strerror(errno.EPIPE))
    return int.from_bytes(byte_array, byteorder="big", signed=True)


def write(writer, data):
    writer.write(data.to_bytes(SIZE, byteorder="big", signed=True))
    writer.flush()
