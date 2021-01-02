# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later


SIZE = 4


def read(reader):
    return int.from_bytes(reader.read(SIZE), byteorder='big', signed=True)


def write(writer, data):
    writer.write(data.to_bytes(SIZE, byteorder='big', signed=True))
    writer.flush()
