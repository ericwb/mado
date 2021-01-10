# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import math
import socket
import threading

from des import DesKey

from mado.rfb import ascii_str
from mado.rfb import auth_exception
from mado.rfb import client_init
from mado.rfb import encodings
from mado.rfb import fb_update_req
from mado.rfb import key_event
from mado.rfb import msg_types
from mado.rfb import pointer_event
from mado.rfb import rectangle
from mado.rfb import sec_result
from mado.rfb import sec_types
from mado.rfb import server_init
from mado.rfb import signed32
from mado.rfb import unsigned8
from mado.rfb import unsigned16
from mado.rfb import unsigned32

# Protocol versions supported
RFB_VERSION_3_8 = 'RFB 003.008\n'
RFB_VERSION_3_7 = 'RFB 003.007\n'
RFB_VERSION_3_3 = 'RFB 003.003\n'

RFB_PORT = 5900


class Client(threading.Thread):

    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
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

    def run(self):
        try:
            while self.active:
                msg_type = msg_types.MessageTypes(unsigned8.read(self.reader))

                if msg_type == msg_types.MessageTypes.FRAMEBUFFER_UPDATE:
                    self.handle_fb_update()
                    fb_update = fb_update_req.FramebufferUpdateRequestMsg()
                    fb_update.write(self.writer, 0, 0,
                        self.server_init_msg.fb_width,
                        self.server_init_msg.fb_height)
                elif msg_type == msg_types.MessageTypes.SET_COLOR_MAP_ENTRIES:
                    self.handle_color_map()
                elif msg_type == msg_types.MessageTypes.BELL:
                    self.handle_bell()
                elif msg_type == msg_types.MessageTypes.SERVER_CUT_TEXT:
                    self.handle_cut_text()
        except OSError as error:
            print(error)

    def handle_fb_update(self):
        padding = unsigned8.read(self.reader)
        num_rects = unsigned16.read(self.reader)

        i = 0
        last_rect = False
        while i < num_rects and not last_rect:
            rect = rectangle.Rectangle(self.reader)
            encoding = encodings.EncodingTypes(signed32.read(self.reader))
            bytes_per_pixel = self.server_init_msg.pix_format.bits_per_pixel // 8
            data_size = rect.width * rect.height * bytes_per_pixel
            data = self.reader.read(data_size)
            if encoding == encodings.EncodingTypes.RAW:
                self.callback.fb_update(rect, encoding, data)
            elif encoding == encodings.EncodingTypes.LAST_RECT:
                last_rect = True
            elif encoding == encodings.EncodingTypes.CURSOR:
                mask_size = math.floor((rect.width + 7) / 8) * rect.height
                bitmask = self.reader.read(mask_size)
                self.callback.cur_update(rect, encoding, data, bitmask)
            elif encoding == encodings.EncodingTypes.DESKTOP_NAME:
                desktop_name = ascii_str.read(self.reader)
                # TODO: callback to update desktop name
            i += 1

    def handle_color_map(self):
        pass

    def handle_bell(self):
        pass

    def handle_cut_text(self):
        pass

    def connect(self, hostname, port=RFB_PORT, timeout=15):
        """
        Connect and authenticate to an RFB server.

        :param str hostname: the address to connect to
        :param int port: the port used to connect with (default=5900)
        :param int timeout: the timeout to connect in seconds (default=15)

        :raises socket.gaierror: error occurred getting address
        :raises ConnectionRefusedError: when a socket connection is refused
        :raises TimeoutError: when a socket connection times out
        """

        # Create socket connection
        self.sock = socket.create_connection((hostname, port), timeout)
        self.reader = self.sock.makefile(mode='rb')
        self.writer = self.sock.makefile(mode='wb')

        # Read server's version string
        self.proto_ver = ascii_str.read_ver(self.reader)
        print('protocol version: {}'.format(self.proto_ver))

        sec_type = sec_types.SecTypes.INVALID
        if self.proto_ver in (RFB_VERSION_3_8, RFB_VERSION_3_7):
            ascii_str.write_ver(self.writer, self.proto_ver)

            num_sec_types = unsigned8.read(self.reader)
            sectypes = [None] * num_sec_types
            print('number of security types: %d' % num_sec_types)

            for i in range(num_sec_types):
                sectypes[i] = sec_types.SecTypes(unsigned8.read(self.reader))
                print('sectypes[i]: %s' % sectypes[i])

            for i in range(num_sec_types):
                if sectypes[i] == sec_types.SecTypes.VNC_AUTH:
                    sec_type = sec_types.SecTypes.VNC_AUTH
                    break
                if sectypes[i] == sec_types.SecTypes.NONE:
                    sec_type = sec_types.SecTypes.NONE
                    break
            unsigned8.write(self.writer, sec_type.value)
        elif self.proto_ver == RFB_VERSION_3_3:
            ascii_str.write_ver(self.writer, self.proto_ver)
            sec_type = unsigned32.read(self.reader)
        else:
            # TODO: error unsupported version
            print('error: unsupported version: {}'.format(self.proto_ver))
        return sec_type

    def no_auth(self):
        # Read security result
        secresult = sec_result.SecResult(unsigned32.read(self.reader))

        if secresult == sec_result.SecResult.OK:
            self._do_init()
        else:
            if self.proto_ver == RFB_VERSION_3_8:
                reason = ascii_str.read(self.reader)
                print('reason: %s' % reason)
            raise auth_exception.AuthException(secresult, reason)

    def vnc_auth(self, password):
        challenge = self.reader.read(16)

        # Truncate passwords longer than 64 bits and pad short than 64 bits
        password = '{:\0<8}'.format(password)[:8].encode()

        # Note: The lowest bit of each byte is considered the first bit
        # and the highest discarded as parity. This is the reverse order
        # of most implementations of DES so the key may require adjustment
        # to give the expected result.
        passkey = []
        for c in password:
            passkey.append(int('{:08b}'.format(c)[::-1], 2))
        key = DesKey(bytes(passkey))
        result = key.encrypt(challenge)
        self.writer.write(result)
        self.writer.flush()

        # Read security result
        secresult = sec_result.SecResult(unsigned32.read(self.reader))

        if secresult == sec_result.SecResult.OK:
            self._do_init()
        else:
            if self.proto_ver == RFB_VERSION_3_8:
                reason = ascii_str.read(self.reader)
                print('reason: %s' % reason)
            raise auth_exception.AuthException(secresult, reason)

    def _do_init(self):
        # Write client initialization message
        client_init_msg = client_init.ClientInitMsg()
        client_init_msg.write(self.writer)

        # Read server initialization message
        self.server_init_msg = server_init.ServerInitMsg(self.reader)
        print(self.server_init_msg)

        # Start the handler thread
        self.start_thread()

        # Send supported encodings
        set_encodings = encodings.SetEncodings()
        supported_encodings = [
            encodings.EncodingTypes.RAW,
            encodings.EncodingTypes.DESKTOP_SIZE,
            encodings.EncodingTypes.LAST_RECT,
            encodings.EncodingTypes.CURSOR,
            encodings.EncodingTypes.DESKTOP_NAME,
            encodings.EncodingTypes.XVP,
            encodings.EncodingTypes.CONTINUOUS_UPDATES,
        ]
        set_encodings.write(self.writer, supported_encodings)

        # Request first update
        fb_upd_req = fb_update_req.FramebufferUpdateRequestMsg()
        fb_upd_req.write(self.writer, 0, 0, self.server_init_msg.fb_width,
            self.server_init_msg.fb_height, False)

    def key_down(self, key):
        kevent = key_event.KeyEvent()
        kevent.write(self.writer, down_flag=True, key=key)

    def key_up(self, key):
        kevent = key_event.KeyEvent()
        kevent.write(self.writer, down_flag=False, key=key)

    def mouse_move(self, button_mask, x, y):
        pevent = pointer_event.PointerEvent()
        pevent.write(self.writer, button_mask, x, y)

    def close(self):
        self.stop_thread()
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)
        if self.sock:
            self.sock.close()
