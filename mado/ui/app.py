# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import tkinter
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

from mado.transport import callback
from mado.transport import client


DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


class App(callback.ClientCallback):

    def __init__(self):
        # Create the main window
        self.window = tkinter.Tk()
        self.window.title("Mado")
        self.window.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

        # Add the menu bar
        self.add_menu_bar()

        # Establish a connection
        self.rdp = client.Client(self)
        try:
            self.rdp.connect('10.33.110.193')
            self.resize(self.rdp.server_init_msg.fb_width, self.rdp.server_init_msg.fb_height)
            self.canvas = tkinter.Canvas(self.window, width=self.rdp.server_init_msg.fb_width, height=self.rdp.server_init_msg.fb_height)
            self.main_img = Image.new(mode='RGBA', size=(self.rdp.server_init_msg.fb_width, self.rdp.server_init_msg.fb_height))
            self.canvas.pack(expand=True, fill=tkinter.BOTH)
            self.window.title(self.rdp.server_init_msg.name)

            # Bind key and mouse events to window
            self.window.bind('<KeyPress>', self.key_down)
            self.window.bind('<KeyRelease>', self.key_up)
            self.window.bind('<Motion>', self.handle_mousemove)
            self.window.mainloop()
        except OSError as error:
            messagebox.showerror()
            # messagebox.showinfo(title='Error', message=error.strerror)
            self.rdp.close()

    # Add menubar and menu items
    def add_menu_bar(self):
        self.window.option_add('*tearOff', False)
        self.window.createcommand('tk::mac::ShowPreferences', self.show_preferences)

        menubar = tkinter.Menu(self.window)
        app_menu = tkinter.Menu(menubar, name='apple')
        menubar.add_cascade(menu=app_menu)
        app_menu.add_command(label='About Mado')
        app_menu.add_separator()

        file_menu = tkinter.Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_separator()

        window_menu = tkinter.Menu(menubar, name='window')
        menubar.add_cascade(label='Window', menu=window_menu)

        help_menu = tkinter.Menu(menubar, name='help')
        menubar.add_cascade(label='Help', menu=help_menu)
        self.window.createcommand('tk::mac::ShowHelp', self.about)

        self.window['menu'] = menubar
        self.window.config(menu=menubar)

    def open_file(self):
        print('open file')
        # host_port = parsed.address[0].split(':')
        # hostname = host_port[0]
        # port = int(host_port[1]) if len(host_port) > 1 else DEFAULT_PORT

    def about(self):
        print("This is a simple example of a menu")

    def show_preferences(self):
        pass

    def resize(self, width, height):
        frm_width = self.window.winfo_rootx() - self.window.winfo_x()
        win_width = width + 2 * frm_width

        titlebar_height = self.window.winfo_rooty() - self.window.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = self.window.winfo_screenwidth() // 2 - win_width // 2
        y = self.window.winfo_screenheight() // 2 - win_height // 2

        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.window.maxsize(width, height)

    def key_down(self, event):
        """Print the character associated to the key pressed"""
        print(event)
        self.rdp.key_down(event.keysym)

    def key_up(self, event):
        """Print the character associated to the key pressed"""
        print(event)
        self.rdp.key_up(event.keysym)

    def handle_mousemove(self, event):
        """Print the character associated to the key pressed"""
        #print(event)
        pass

    def fb_update(self, rect, encoding, data):
        # this might be faster if data is a series of ints
        #self.main_img.paste(data, box=(rect.x, rect.y, rect.width, rect.height))
        image = Image.frombytes(
            mode='RGBA',
            size=(rect.width, rect.height),
            data=data,
            decoder_name=encoding.name.lower()
        )
        self.main_img.paste(image, (rect.x, rect.y))
        self.tkimage = ImageTk.PhotoImage(image=self.main_img)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tkimage)


def main():
    app = App()
