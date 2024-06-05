# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import getpass
import os
import plistlib
import tkinter
import traceback
from tkinter import messagebox
from tkinter import simpledialog

from PIL import Image
from PIL import ImageTk

from mado.rfb import auth_exception
from mado.rfb import callback
from mado.rfb import client
from mado.rfb import sec_types
from mado.ui import login


APP_NAME = "Mado"
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480

PLIST_FILE = "/Users/{}/Library/Preferences/com.github.mado.plist".format(
    getpass.getuser()
)


class App(callback.ClientCallback):
    def __init__(self):
        # Create the main window
        self.window = tkinter.Tk()
        self.window.title(APP_NAME)
        self.window.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.canvas = tkinter.Canvas(
            self.window,
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            highlightthickness=0,
        )
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

        # Create our property list file if not exists
        if not os.path.exists(PLIST_FILE):
            with open(PLIST_FILE, "wb") as file:
                data = {}
                data["recent"] = {}
                plistlib.dump(data, file)

        # Add the menu bar
        self.add_menu_bar()

        # Start the main event loop
        self.window.mainloop()

    # Add menubar and menu items
    def add_menu_bar(self):
        self.window.option_add("*tearOff", False)
        self.window.createcommand(
            "tk::mac::ShowPreferences", self._show_preferences
        )

        menubar = tkinter.Menu(self.window)
        app_menu = tkinter.Menu(menubar, name="apple")
        menubar.add_cascade(menu=app_menu)
        app_menu.add_command(label=f"About {APP_NAME}")
        app_menu.add_separator()

        # Create the file menu and its menu items
        self.file_menu = tkinter.Menu(menubar)
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="Open...", command=self._open_connection
        )
        self.recent_menu = tkinter.Menu(self.file_menu)
        self.file_menu.add_cascade(menu=self.recent_menu, label="Open Recent")

        with open(PLIST_FILE, "rb") as file:
            data = plistlib.load(file)
        for key, value in data["recent"].items():
            self.recent_menu.add_command(
                label=key, command=lambda x=value: self._connect(x)
            )

        self.recent_menu.add_separator()
        self.recent_menu.add_command(
            label="Clear items", command=self._clear_recent
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Close", command=self._close_connection
        )
        self.file_menu.entryconfigure("Close", state=tkinter.DISABLED)

        # Create the window menu and its menu items
        window_menu = tkinter.Menu(menubar, name="window")
        menubar.add_cascade(label="Window", menu=window_menu)

        # Create the help menu and its menu items
        help_menu = tkinter.Menu(menubar, name="help")
        menubar.add_cascade(label="Help", menu=help_menu)
        self.window.createcommand("tk::mac::ShowHelp", self._about)

        self.window["menu"] = menubar
        self.window.config(menu=menubar)

    def _open_connection(self):
        address = simpledialog.askstring("Open", "Hostname:")
        if address:
            self._connect(address)

    def _connect(self, address):
        print(address)
        host_port = address.split(":")
        hostname = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else client.RFB_PORT

        # Initialize client
        self.rfb = client.Client(self)

        try:
            # Establish a connection
            sec_type = self.rfb.connect(hostname, port)
            print(f"sec_type: {sec_type}")

            authenticated = False
            if sec_type == sec_types.SecTypes.DIFFIE_HELLMAN_AUTH:
                while not authenticated:
                    cred = login.LoginDialog(
                        self.window, title="Authentication"
                    )
                    try:
                        self.rfb.dh_auth(cred.username, cred.password)
                        authenticated = True
                    except auth_exception.AuthException as auth_exc:
                        print("AuthException")
                        print(auth_exc.secresult)
                        print(auth_exc.reason)
            elif sec_type == sec_types.SecTypes.VNC_AUTH:
                while not authenticated:
                    password = simpledialog.askstring(
                        "Authentication", "Password:", show="*"
                    )
                    try:
                        self.rfb.vnc_auth(password)
                        authenticated = True
                    except auth_exception.AuthException as auth_exc:
                        print("AuthException")
                        print(auth_exc.secresult)
                        print(auth_exc.reason)
            elif sec_type == sec_types.SecTypes.NONE:
                try:
                    self.rfb.no_auth()
                    authenticated = True
                except auth_exception.AuthException as auth_exc:
                    print(auth_exc.secresult)
                    print(auth_exc.reason)
            else:
                # TODO: raise exception
                print(f"Unknown security type: {sec_type}")

            if authenticated:
                # Set window dimensions
                self.resize(self.rfb.fb_width, self.rfb.fb_height)
                self.main_img = Image.new(
                    mode="RGBX", size=(self.rfb.fb_width, self.rfb.fb_height)
                )
                self.canvas.pack(expand=True, fill=tkinter.BOTH)

                # Determine image mode
                pix_fmt = self.rfb.pix_format
                if (
                    pix_fmt.depth == 24
                    and not pix_fmt.big_endian
                    and pix_fmt.true_color
                    and pix_fmt.red_max == 255
                    and pix_fmt.green_max == 255
                    and pix_fmt.blue_max == 255
                ):
                    self.image_mode = list("RGB")
                    self.image_mode[pix_fmt.red_shift // 8] = "R"
                    self.image_mode[pix_fmt.green_shift // 8] = "G"
                    self.image_mode[pix_fmt.blue_shift // 8] = "B"
                    self.image_mode = "".join(self.image_mode) + "X"

                # Set the winow title
                self.window.title(self.rfb.display_name)

                # Bind key and mouse events to window
                self.window.bind("<KeyPress>", self._on_key_down)
                self.window.bind("<KeyRelease>", self._on_key_up)
                self.window.bind("<Motion>", self._on_mouse_move)
                self.window.bind("<MouseWheel>", self._on_mouse_wheel)
                self.window.bind("<ButtonPress>", self._on_mouse_down)
                self.window.bind("<ButtonRelease>", self._on_mouse_up)

                # Enable the Close menu item
                self.file_menu.entryconfigure("Close", state=tkinter.NORMAL)

                # Add to list of recent connections
                self._add_to_recent(self.rfb.display_name, address)
        except OSError as error:
            traceback.print_exc()
            messagebox.showwarning(title="Error", message=error.strerror)
            self.rfb.close()

    def _close_connection(self):
        # Disable close menu item
        self.file_menu.entryconfigure("Close", state=tkinter.DISABLED)

        # Unbind key and mouse events
        self.window.unbind("<KeyPress>")
        self.window.unbind("<KeyRelease>")
        self.window.unbind("<Motion>")
        self.window.unbind("<MouseWheel>")
        self.window.unbind("<ButtonPress>")
        self.window.unbind("<ButtonRelease>")

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

        self.window.geometry(f"{width}x{height}+{x}+{y}")
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
        # print(event)
        if event.x >= 0 and event.y >= 0:
            # TODO: need to swap buttons 2 and 3
            if event.state == 256:
                self.rfb.mouse_move(1, event.x, event.y)
            elif event.state == 512:
                self.rfb.mouse_move(2, event.x, event.y)
            elif event.state == 1024:
                self.rfb.mouse_move(3, event.x, event.y)
            else:
                self.rfb.mouse_move(0, event.x, event.y)

    def _on_mouse_wheel(self, event):
        # print(event)
        if event.x >= 0 and event.y >= 0:
            for _ in range(abs(event.delta)):
                self.rfb.mouse_down(
                    4 if event.delta > 0 else 5, event.x, event.y
                )
                self.rfb.mouse_up(
                    4 if event.delta > 0 else 5, event.x, event.y
                )

    def _on_mouse_down(self, event):
        # print(event)
        if event.x >= 0 and event.y >= 0:
            # Swap buttons 2 and 3
            num = 2 if event.num == 3 else event.num
            num = 3 if event.num == 2 else event.num
            self.rfb.mouse_down(num, event.x, event.y)

    def _on_mouse_up(self, event):
        # print(event)
        if event.x >= 0 and event.y >= 0:
            # Swap buttons 2 and 3
            num = 2 if event.num == 3 else event.num
            num = 3 if event.num == 2 else event.num
            self.rfb.mouse_up(num, event.x, event.y)

    def _add_to_recent(self, display_name, address):
        with open(PLIST_FILE, "rb") as file:
            data = plistlib.load(file)
        if display_name not in data["recent"]:
            self.recent_menu.insert(
                0,
                "command",
                label=display_name,
                command=lambda x=address: self._connect(x),
            )
            data["recent"][display_name] = address
            with open(PLIST_FILE, "wb") as file:
                plistlib.dump(data, file)

    def _clear_recent(self):
        with open(PLIST_FILE, "rb") as file:
            data = plistlib.load(file)
        for item in data["recent"]:
            self.recent_menu.delete(item)
        with open(PLIST_FILE, "wb") as file:
            data["recent"] = {}
            plistlib.dump(data, file)

    def get_password(self):
        return simpledialog.askstring("Authentication", "Password:", show="*")

    def fb_update(self, rect, data):
        image = Image.frombytes(
            "RGB", (rect.width, rect.height), data, "raw", self.image_mode
        )

        self.main_img.paste(image, (rect.x, rect.y))
        self.tkimage = ImageTk.PhotoImage(image=self.main_img)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tkimage)

    def fb_copy(self, src_x, src_y, rect):
        image = self.main_img.crop((src_x, src_y, rect.width, rect.height))
        self.main_img.paste(image, (rect.x, rect.y))
        self.tkimage = ImageTk.PhotoImage(image=self.main_img)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tkimage)

    def cur_update(self, rect, data, bitmask):
        pass

    def bell():
        print("\a")


def main():
    app = App()
