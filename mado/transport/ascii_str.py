# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import unsigned32


def read_ver(reader):
    return str(reader.read(12), encoding='ascii')


def write_ver(writer, data):
    writer.write(data.encode())
    writer.flush()


def read(reader):
    length = unsigned32.read(reader)
    return reader.read(length).decode('ascii')


def write(writer, data):
    unsigned32.write(writer, len(data))
    writer.send(data.encode(encoding='UTF-8'))
    writer.flush()
