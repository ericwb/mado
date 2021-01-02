# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import objc
import Cocoa
import AppKit
from AppKit import NSAlert
from AppKit import NSApp
from AppKit import NSApplication
from AppKit import NSImage
from AppKit import NSObject
from AppKit import NSWindow
from AppKit import NSCriticalAlertStyle
from AppKit import NSAlertStyleCritical
from AppKit import NSAlertStyleWarning
from AppKit import NSImageNameCaution
from PyObjCTools import AppHelper

from mado.transport import client


DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


"""
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
"""


def open_file():
    print('open file')
    # host_port = parsed.address[0].split(':')
    # hostname = host_port[0]
    # port = int(host_port[1]) if len(host_port) > 1 else DEFAULT_PORT


def about():
    print("This is a simple example of a menu")


def show_preferences():
    pass


def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event)


def handle_mousemove(event):
    """Print the character associated to the key pressed"""
    print(event)


# Add menubar and menu items
"""
def add_menu_bar(window):
    window.option_add('*tearOff', False)
    window.createcommand('tk::mac::ShowPreferences', show_preferences)

    menubar = tkinter.Menu(window)
    app_menu = tkinter.Menu(menubar, name='apple')
    menubar.add_cascade(menu=app_menu)
    app_menu.add_command(label='About Mado')
    app_menu.add_separator()

    file_menu = tkinter.Menu(menubar)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open...", command=open_file)
    file_menu.add_separator()

    window_menu = tkinter.Menu(menubar, name='window')
    menubar.add_cascade(label='Window', menu=window_menu)

    help_menu = tkinter.Menu(menubar, name='help')
    menubar.add_cascade(label='Help', menu=help_menu)
    window.createcommand('tk::mac::ShowHelp', about)

    window['menu'] = menubar
    window.config(menu=menubar)
"""


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        print("Hello, World!")

    def sayHello_(self, sender):
        print("Hello again, World!")


def main():
    # Create the main window
    app = NSApplication.sharedApplication()

    # we must keep a reference to the delegate object ourselves,
    # NSApp.setDelegate_() doesn't retain it. A local variable is
    # enough here.
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)

    window = NSWindow.alloc()
    content_rect = ((200.0, 300.0), (DEFAULT_WIDTH, DEFAULT_HEIGHT))
    window.initWithContentRect_styleMask_backing_defer_(content_rect, 15, 2, 0)
    window.setTitle_('Mado')
    window.setLevel_(3)  # floating window

    # window.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    # resize(window, DEFAULT_WIDTH, DEFAULT_HEIGHT)

    # Add the menu bar
    # add_menu_bar(window)

    # Establish a connection
    rdp = client.Client()
    try:
        rdp.connect('10.33.110.193', 5905)
        # resize(window, rdp.server_init_msg.fb_width, rdp.server_init_msg.fb_height)
        window.setTitle_(rdp.server_init_msg.name)

        # Bind key and mouse events to window
        # window.bind('<Key>', handle_keypress)
        # window.bind('<Motion>', handle_mousemove)
        # window.mainloop()
        window.display()
        window.orderFrontRegardless()

        AppHelper.runEventLoop()

    except OSError as error:
        title = None
        ok = None
        cancel = None
        other = None
        message = error.strerror
        alert = NSAlert.alloc().init()
        #alert.setAlertStyle_(2)
        alert.setMessageText_(message)
        #alert.setInformativeText_(message)
        alert.window().setAppearance_(AppKit.NSAppearance.currentAppearance())
        #alert.setIcon_(NSImage.imageNamed_(NSImageNameCaution))
        alert.runModal()
        # messagebox.showinfo(icon=messagebox.ERROR)
        # messagebox.showinfo(title='Error', message=error.strerror)
        rdp.close()
