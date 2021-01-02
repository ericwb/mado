# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later


SIZE = 2


def read(reader):
    return int.from_bytes(reader.read(SIZE), byteorder='big', signed=False)


def write(writer, data):
    writer.write(data.to_bytes(SIZE, byteorder='big', signed=False))
    writer.flush()
