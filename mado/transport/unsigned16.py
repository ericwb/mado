# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later


SIZE = 2


def read(reader):
    byte_array = bytearray(SIZE)
    return readinto(reader, byte_array)


def readinto(reader, byte_array):
    bytes_read = reader.readinto(byte_array)
    if bytes_read <= 0:
        raise BrokenPipeError(32, 'Broken pipe')

    return int.from_bytes(byte_array, byteorder='big', signed=False)


def write(writer, data):
    writer.write(data.to_bytes(SIZE, byteorder='big', signed=False))
    writer.flush()
