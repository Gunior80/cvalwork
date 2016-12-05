#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygtk
import gtk
from logic import *


if __name__ == '__main__':
    window = Driver()
    window.connect("delete-event", gtk.main_quit)
    window.show_all()
    gtk.main()




