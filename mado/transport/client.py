# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import socket
import threading

from mado.transport import ascii_str
from mado.transport import client_init
from mado.transport import msg_types
from mado.transport import sec_result
from mado.transport import sec_types
from mado.transport import server_init
from mado.transport import unsigned8
from mado.transport import unsigned32


# Protocol versions supported
RFB_VERSION_3_8 = 'RFB 003.008\n'
RFB_VERSION_3_7 = 'RFB 003.007\n'
RFB_VERSION_3_3 = 'RFB 003.003\n'

RDP_PORT = 5900


class Client(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.setDaemon(True)
        self.active = False

    def start_thread(self):
        self.active = True
        self.start()

    def stop_thread(self):
        self.active = True
        self.join()

    def run(self):
        while self.active:
            msg_type = msg_types.MessageTypes(unsigned8.read(self.sock))
            print(msg_type)

            if msg_type == msg_types.MessageTypes.FRAMEBUFFER_UPDATE:
                pass
            elif msg_type == msg_types.MessageTypes.SET_COLOUR_MAP_ENTRIES:
                pass
            elif msg_type == msg_types.MessageTypes.BELL:
                pass
            elif msg_type == msg_types.MessageTypes.SERVER_CUT_TEXT:
                pass

    def connect(self, hostname, port=RDP_PORT, username=None, password=None,
                timeout=None):
        """
        Connect and authenticate to an RFB server.

        :param str hostname: the address to connect to
        :param int port: the port used to connect with
        :param str username: the username to authenticate with
        :param str password: the password to authenticate with
        :param int timeout: the timeout for the connection in seconds

        :raises socket.gaierror: error occurred getting address
        :raises ConnectionRefusedError: when a socket connection is refused
        :raises TimeoutError: when a socket connection times out
        """

        # Create socket connection
        self.sock = socket.create_connection((hostname, port), timeout)

        # Read server's version string
        proto_ver = ascii_str.read_ver(self.sock)
        print('protocol version: %s' % proto_ver)

        sec_type = sec_types.SecTypes.INVALID
        if proto_ver in (RFB_VERSION_3_8, RFB_VERSION_3_7):
            ascii_str.write_ver(self.sock, proto_ver)

            num_sec_types = unsigned8.read(self.sock)
            sectypes = [None] * num_sec_types
            print('number of security types: %d' % num_sec_types)

            for i in range(0, num_sec_types):
                sectypes[i] = sec_types.SecTypes(unsigned8.read(self.sock))
                print('sectypes[i]: %s' % sectypes[i])

            for i in range(0, num_sec_types):
                # TODO: decide security type
                if sectypes[i] == sec_types.SecTypes.NONE:
                    sec_type = sec_types.SecTypes.NONE
                    break
                if sectypes[i] == sec_types.SecTypes.VNC_AUTH:
                    sec_type = sec_types.SecTypes.VNC_AUTH
                    break
            unsigned8.write(self.sock, sec_type.value)
        elif proto_ver == RFB_VERSION_3_3:
            ascii_str.write_ver(self.sock, proto_ver)
        else:
            print('error')

        print(sectypes)
        if sectypes == sec_types.SecTypes.VNC_AUTH:
            challenge = [None] * 16
            for i in range(0, 16):
                challenge[i] = unsigned8.read(self.sock)
            print(challenge)

        # Read security result
        secresult = sec_result.SecResult.OK
        if proto_ver == RFB_VERSION_3_8:
            secresult = sec_result.SecResult(unsigned32.read(self.sock))
            print('secresult: %s' % secresult)

        if secresult == sec_result.SecResult.OK:
            # Write client initialization message
            client_init_msg = client_init.ClientInitMsg()
            client_init_msg.write(self.sock)

            # Read server initialization message
            self.server_init_msg = server_init.ServerInitMsg(self.sock)
            print(self.server_init_msg)

            # transport = Transport(self.sock)
            # transport.start_thread()
        else:
            if proto_ver == RFB_VERSION_3_8:
                print('Authentication failed: %s' % ascii_str.read(self.sock))
            else:
                print('Authentication failed')

    def close(self):
        if self.sock:
            self.sock.close()
