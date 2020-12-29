# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
from signal import signal
from signal import SIGINT
import socket
import sys
import threading

import tkinter

import ascii_str
from client_init import ClientInitMsg
import msg_types
from sec_result import SecResult
from sec_types import SecTypes
from server_init import ServerInitMsg
import unsigned8
import unsigned32


# Protocol versions supported
RFB_VERSION_3_8 = 'RFB 003.008\n'
RFB_VERSION_3_7 = 'RFB 003.007\n'
RFB_VERSION_3_3 = 'RFB 003.003\n'

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_PORT = 5900


class Transport(threading.Thread):

    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sock = sock
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


def resize(window, width, height):
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2 * frm_width

    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width

    print(window.winfo_screenwidth())
    print(window.winfo_screenheight())

    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2

    print(x)
    print(y)

    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.maxsize(width, height)


# Main code execution
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'address',
        action='store',
        nargs=1,
        help='Address and port for connection (<address:port>).'
    )
    parsed = parser.parse_args()

    host_port = parsed.address[0].split(':')
    hostname = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else DEFAULT_PORT

    window = tkinter.Tk()
    window.title("Mado")
    window.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    resize(window, DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def showMyPreferencesDialog():
        pass

    window.option_add('*tearOff', False)
    window.createcommand('tk::mac::ShowPreferences', showMyPreferencesDialog)

    menubar = tkinter.Menu(window)
    app_menu = tkinter.Menu(menubar, name='apple')
    menubar.add_cascade(menu=app_menu)
    app_menu.add_command(label='About Mado')
    app_menu.add_separator()

    def OpenFile():
        print(name)

    file_menu = tkinter.Menu(menubar)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open...", command=OpenFile)
    file_menu.add_separator()

    window_menu = tkinter.Menu(menubar, name='window')
    menubar.add_cascade(label='Window', menu=window_menu)

    def About():
        print("This is a simple example of a menu")

    help_menu = tkinter.Menu(menubar, name='help')
    menubar.add_cascade(label='Help', menu=help_menu)
    window.createcommand('tk::mac::ShowHelp', About)

    window['menu'] = menubar
    window.config(menu=menubar)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname, port))
        proto_ver = ascii_str.read_ver(sock)
        print('protocol version: %s' % proto_ver)

        sec_type = SecTypes.INVALID
        if proto_ver in (RFB_VERSION_3_8, RFB_VERSION_3_7):
            ascii_str.write_ver(sock, proto_ver)

            num_sec_types = unsigned8.read(sock)
            sec_types = [None] * num_sec_types
            print('number of security types: %d' % num_sec_types)

            for i in range(0, num_sec_types):
                sec_types[i] = SecTypes(unsigned8.read(sock))
                print('sec_types[i]: %s' % sec_types[i])

            for i in range(0, num_sec_types):
                # TODO: decide security type
                if sec_types[i] == SecTypes.NONE:
                    sec_type = SecTypes.NONE
                    break
                elif sec_types[i] == SecTypes.VNC_AUTH:
                    sec_type = SecTypes.VNC_AUTH
                    break
            unsigned8.write(sock, sec_type.value)
        elif proto_ver == RFB_VERSION_3_3:
            ascii_str.write_ver(sock, proto_ver)
        else:
            print('error')

        print(sec_type)
        if sec_type == SecTypes.VNC_AUTH:
            challenge = [None] * 16
            for i in range(0, 16):
                challenge[i] = unsigned8.read(sock)
            print(challenge)

        # Read security result
        sec_result = SecResult.OK
        if proto_ver == RFB_VERSION_3_8:
            sec_result = SecResult(unsigned32.read(sock))
            print('sec_result: %s' % sec_result)

        if sec_result == SecResult.OK:
            # Write client initialization message
            client_init_msg = ClientInitMsg()
            client_init_msg.write(sock)

            # Read server initialization message
            server_init_msg = ServerInitMsg(sock)
            print(server_init_msg)

            def handle_keypress(event):
                """Print the character associated to the key pressed"""
                print(event)

            def handle_mousemove(event):
                """Print the character associated to the key pressed"""
                print(event)

            #resize(window, server_init_msg.fb_width, server_init_msg.fb_height)
            window.title(server_init_msg.name)

            # Bind keypress event to handle_keypress()
            #window.bind('<Key>', handle_keypress)
            #window.bind('<Motion>', handle_mousemove)

            #transport = Transport(sock)
            #transport.start_thread()
            window.mainloop()
        else:
            if proto_ver == RFB_VERSION_3_8:
                print('Authentication failed: %s' % ascii_str.read(sock))
            else:
                print('Authentication failed')


def handler(signal_received, frame):
    # Handle any cleanup here
    sys.exit(0)


if __name__ == '__main__':
    signal(SIGINT, handler)
    main()
