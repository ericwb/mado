# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.rfb import unsigned32


def read_ver(reader):
    return str(reader.readline(12), encoding='ascii')


def write_ver(writer, data):
    writer.write(data.encode('ascii'))
    writer.flush()


def read(reader):
    length = unsigned32.read(reader)
    byte_array = bytearray(length)
    return readinto(reader, byte_array)


def readinto(reader, byte_array):
    bytes_read = reader.readinto(byte_array)
    if bytes_read <= 0:
        raise BrokenPipeError(32, 'Broken pipe')

    return byte_array.decode('utf-8')


def write(writer, data):
    unsigned32.write(writer, len(data))
    writer.send(data.encode(encoding='utf-8'))
    writer.flush()
