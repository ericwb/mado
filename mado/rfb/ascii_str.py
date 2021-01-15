# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import errno
import os
import struct

from mado.rfb import unsigned32


def read_ver(reader):
    return str(reader.readline(12), encoding='ascii')


def write_ver(writer, data):
    writer.write(data.encode('ascii'))
    writer.flush()


def read(reader):
    length = unsigned32.read(reader)
    return read_len(reader, length)


def read_len(reader, length):
    byte_array = bytearray(length)
    return readinto(reader, byte_array)


def readinto(reader, byte_array):
    if reader.readinto(byte_array) <= 0:
        raise BrokenPipeError(errno.EPIPE, os.strerror(errno.EPIPE))
    (string,) = struct.unpack('!{}s'.format(len(byte_array)), byte_array)
    return string.decode('utf-8')


def write(writer, data):
    writer.write(struct.pack('!I{}s'.format(len(data)), len(data), data))
    writer.flush()
