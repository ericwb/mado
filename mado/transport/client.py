# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import socket
import threading

from mado.transport import ascii_str
from mado.transport import client_init
from mado.transport import encodings
from mado.transport import fb_update_req
from mado.transport import msg_types
from mado.transport import rectangle
from mado.transport import sec_result
from mado.transport import sec_types
from mado.transport import server_init
from mado.transport import signed32
from mado.transport import unsigned8
from mado.transport import unsigned16
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
        self.reader = None
        self.writer = None
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
            msg_type = msg_types.MessageTypes(unsigned8.read(self.reader))
            print(msg_type)

            if msg_type == msg_types.MessageTypes.FRAMEBUFFER_UPDATE:
                self.handle_fb_update()
            elif msg_type == msg_types.MessageTypes.SET_COLOUR_MAP_ENTRIES:
                self.handle_color_map()
            elif msg_type == msg_types.MessageTypes.BELL:
                self.handle_bell()
            elif msg_type == msg_types.MessageTypes.SERVER_CUT_TEXT:
                self.handle_cut_text()

    def handle_fb_update(self):
        padding = unsigned8.read(self.reader)
        for _ in range(unsigned16.read(self.reader)):
            rect = rectangle.Rectangle(self.reader)
            encoding = encodings.EncodingTypes(signed32.read(self.reader))
            bytes_per_pixel = self.server_init_msg.pix_format.bits_per_pixel // 8
            data_size = rect.width * rect.height * bytes_per_pixel
            data = self.reader.read(data_size)
            #callback.fb_update(rect, encoding, data)

            print(rect)
            print(encoding)
            #from PIL import Image
            #from PIL import ImageShow
            #image = Image.frombytes(mode='RGBA', size=(rects[i].width, rects[i].height), data=data, decoder_name='raw')
            #ImageShow.show(image, title=None)

    def handle_color_map(self):
        pass

    def handle_bell(self):
        pass

    def handle_cut_text(self):
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
        self.reader = self.sock.makefile(mode='rb')
        self.writer = self.sock.makefile(mode='wb')

        # Read server's version string
        proto_ver = ascii_str.read_ver(self.reader)
        print('protocol version: {}'.format(proto_ver))

        sec_type = sec_types.SecTypes.INVALID
        if proto_ver in (RFB_VERSION_3_8, RFB_VERSION_3_7):
            ascii_str.write_ver(self.writer, proto_ver)

            num_sec_types = unsigned8.read(self.reader)
            sectypes = [None] * num_sec_types
            print('number of security types: %d' % num_sec_types)

            for i in range(num_sec_types):
                sectypes[i] = sec_types.SecTypes(unsigned8.read(self.reader))
                print('sectypes[i]: %s' % sectypes[i])

            for i in range(num_sec_types):
                # TODO: decide security type
                if sectypes[i] == sec_types.SecTypes.NONE:
                    sec_type = sec_types.SecTypes.NONE
                    break
                if sectypes[i] == sec_types.SecTypes.VNC_AUTH:
                    sec_type = sec_types.SecTypes.VNC_AUTH
                    break
            unsigned8.write(self.writer, sec_type.value)
        elif proto_ver == RFB_VERSION_3_3:
            ascii_str.write_ver(self.writer, proto_ver)
        else:
            print('error')

        print(sectypes)
        if sectypes == sec_types.SecTypes.VNC_AUTH:
            challenge = [None] * 16
            for i in range(16):
                challenge[i] = unsigned8.read(self.reader)
            print(challenge)

        # Read security result
        secresult = sec_result.SecResult.OK
        if proto_ver == RFB_VERSION_3_8:
            secresult = sec_result.SecResult(unsigned32.read(self.reader))
            print('secresult: %s' % secresult)

        if secresult == sec_result.SecResult.OK:
            # Write client initialization message
            client_init_msg = client_init.ClientInitMsg()
            client_init_msg.write(self.writer)

            # Read server initialization message
            self.server_init_msg = server_init.ServerInitMsg(self.reader)
            print(self.server_init_msg)

            # Start the handler thread
            self.start_thread()

            # Request first update
            fb_upd_req = fb_update_req.FramebufferUpdateRequestMsg()
            fb_upd_req.write(self.writer, 0, 0, self.server_init_msg.fb_width, self.server_init_msg.fb_height, False)
        else:
            if proto_ver == RFB_VERSION_3_8:
                print('Authentication failed: %s' % ascii_str.read(self.reader))
            else:
                print('Authentication failed')

    def close(self):
        if self.sock:
            self.sock.close()
