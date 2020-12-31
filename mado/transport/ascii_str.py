# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
from mado.transport import unsigned32


def read_ver(socket):
    return str(socket.recv(12), encoding='ascii')


def write_ver(socket, data):
    socket.send(data.encode())


def read(socket):
    length = unsigned32.read(socket)
    return socket.recv(length).decode('ascii')


def write(socket, data):
    unsigned32.write(socket, len(data))
    socket.send(data.encode())
