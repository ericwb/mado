# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import tkinter
from tkinter import messagebox
from tkinter import simpledialog

from PIL import Image
from PIL import ImageTk

from mado.rfb import auth_exception
from mado.rfb import callback
from mado.rfb import client
from mado.rfb import sec_types


APP_NAME = 'Mado'
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


class App(callback.ClientCallback):

    def __init__(self):
        # Create the main window
        self.window = tkinter.Tk()
        self.window.title(APP_NAME)
        self.window.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.canvas = tkinter.Canvas(self.window, width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT, highlightthickness=0)
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

        # Add the menu bar
        self.add_menu_bar()

        # Start the main event loop
        self.window.mainloop()

    # Add menubar and menu items
    def add_menu_bar(self):
        self.window.option_add('*tearOff', False)
        self.window.createcommand('tk::mac::ShowPreferences',
            self._show_preferences)

        menubar = tkinter.Menu(self.window)
        app_menu = tkinter.Menu(menubar, name='apple')
        menubar.add_cascade(menu=app_menu)
        app_menu.add_command(label='About {}'.format(APP_NAME))
        app_menu.add_separator()

        self.file_menu = tkinter.Menu(menubar)
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open...", command=self._open_connection)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close", command=self._close_connection)
        self.file_menu.entryconfigure('Close', state=tkinter.DISABLED)

        window_menu = tkinter.Menu(menubar, name='window')
        menubar.add_cascade(label='Window', menu=window_menu)

        help_menu = tkinter.Menu(menubar, name='help')
        menubar.add_cascade(label='Help', menu=help_menu)
        self.window.createcommand('tk::mac::ShowHelp', self._about)

        self.window['menu'] = menubar
        self.window.config(menu=menubar)

    def _open_connection(self):
        address = simpledialog.askstring('Open', 'Hostname:')
        if address:
            host_port = address.split(':')
            hostname = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else client.RFB_PORT

            # Initialize client
            self.rfb = client.Client(self)

            try:
                # Establish a connection
                sec_type = self.rfb.connect(hostname, port)
                print('sec_type: {}'.format(sec_type))

                authenticated = False
                if sec_type == sec_types.SecTypes.VNC_AUTH:
                    print('attempting vnc auth')
                    while not authenticated:
                        password = simpledialog.askstring('Authentication',
                            'Password:', show='*')
                        try:
                            self.rfb.vnc_auth(password)
                            authenticated = True
                        except auth_exception.AuthException as auth_exc:
                            print('AuthException')
                            print(auth_exc.secresult)
                            print(auth_exc.reason)
                elif sec_type == sec_types.SecTypes.NONE:
                    print('attempting no auth')
                    try:
                        self.rfb.no_auth()
                        authenticated = True
                    except auth_exception.AuthException as auth_exc:
                        print(auth_exc.secresult)
                        print(auth_exc.reason)
                else:
                    print('Unknown security type: {}'.format(sec_type))

                if authenticated:
                    # Set window dimensions
                    self.resize(self.rfb.server_init_msg.fb_width,
                        self.rfb.server_init_msg.fb_height)
                    self.main_img = Image.new(mode='RGBX',
                        size=(self.rfb.server_init_msg.fb_width,
                            self.rfb.server_init_msg.fb_height))
                    self.canvas.pack(expand=True, fill=tkinter.BOTH)

                    # Determine image mode
                    pix_fmt = self.rfb.server_init_msg.pix_format
                    if (pix_fmt.depth == 24 and not pix_fmt.big_endian and
                            pix_fmt.true_color and pix_fmt.red_max == 255 and
                            pix_fmt.green_max == 255 and pix_fmt.blue_max == 255):
                        self.image_mode = list('RGB')
                        self.image_mode[pix_fmt.red_shift // 8] = 'R'
                        self.image_mode[pix_fmt.green_shift // 8] = 'G'
                        self.image_mode[pix_fmt.blue_shift // 8] = 'B'
                        self.image_mode = ''.join(self.image_mode) + 'X'

                    # Set the winow title
                    self.window.title(self.rfb.server_init_msg.name)

                    # Bind key and mouse events to window
                    self.window.bind('<KeyPress>', self._on_key_down)
                    self.window.bind('<KeyRelease>', self._on_key_up)
                    self.window.bind('<Motion>', self._on_mouse_move)
                    self.window.bind('<Button>', self._on_mouse_button)

                    # Enable the Close menu item
                    self.file_menu.entryconfigure('Close', state=tkinter.NORMAL)
            except OSError as error:
                print(error)
                messagebox.showwarning(title='Error', message=error.strerror)
                self.rfb.close()

    def _close_connection(self):
        # Disable close menu item
        self.file_menu.entryconfigure('Close', state=tkinter.DISABLED)

        # Unbind key and mouse events
        self.window.unbind('<KeyPress>')
        self.window.unbind('<KeyRelease>')
        self.window.unbind('<Motion>')
        self.window.unbind('<Button>')

        # Close the client connection
        self.rfb.close()

        self.tkimage = None
        self.window.title(APP_NAME)
        self.window.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def _about(self):
        print("_about")

    def _show_preferences(self):
        print("_show_preferences")

    def resize(self, width, height):
        frm_width = self.window.winfo_rootx() - self.window.winfo_x()
        win_width = width + 2 * frm_width

        titlebar_height = self.window.winfo_rooty() - self.window.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = self.window.winfo_screenwidth() // 2 - win_width // 2
        y = self.window.winfo_screenheight() // 2 - win_height // 2

        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.window.maxsize(width, height)
        self.canvas.config(width=width, height=height)

    def _on_key_down(self, event):
        """Print the character associated to the key pressed"""
        print(event)
        self.rfb.key_down(event.keysym)

    def _on_key_up(self, event):
        """Print the character associated to the key pressed"""
        print(event)
        self.rfb.key_up(event.keysym)

    def _on_mouse_move(self, event):
        """Print the character associated to the key pressed"""
        print(event)
        if event.x >= 0 and event.y >= 0:
            self.rfb.mouse_move(0, event.x, event.y)

    def _on_mouse_button(self, event):
        print(event)

    def get_password(self):
        return simpledialog.askstring('Authentication', 'Password:', show='*')

    def fb_update(self, rect, encoding, data):
        # This might be faster if data is a series of ints, so the frombytes can
        # be skipped
        #self.main_img.paste(data, box=(rect.x, rect.y, rect.width, rect.height))
        image = Image.frombytes('RGB', (rect.width, rect.height), data,
            encoding.name.lower(), self.image_mode)
        self.main_img.paste(image, (rect.x, rect.y))
        self.tkimage = ImageTk.PhotoImage(image=self.main_img)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tkimage)


def main():
    app = App()
