# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later


SIZE = 4


def read(socket):
    return int.from_bytes(socket.recv(SIZE), byteorder='big', signed=True)


def write(socket, data):
    socket.send(data.to_bytes(SIZE, byteorder='big', signed=True))