#/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileQuit'/>
    </menu>
    <menu action='EditMenu'>
      <menuitem action='SettingsCategories'/>
    </menu>
    <menu action='AboutMenu'>
      <menuitem action='About' />
    </menu>
  </menubar>
</ui>
"""

class Window(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_size_request(500, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        
        ui_manager = self.create_ui_manager()
        menubar = ui_manager.get_widget("/MenuBar")

        box = gtk.VBox()
        box.pack_start(menubar, False, False, 0)

        self.a = gtk.DrawingArea()
        self.a.set_size_request(20,20)
        

        self.add(box)
    def create_ui_manager(self):
        ui_manager = gtk.UIManager()
        ui_manager.add_ui_from_string(UI_INFO)
        accelgroup = ui_manager.get_accel_group()
        self.add_accel_group(accelgroup)
        action_group = gtk.ActionGroup('MenuBar')
        self.add_file_menu_actions(action_group)
        self.add_edit_menu_actions(action_group)
        self.add_about_menu_actions(action_group)
        ui_manager.insert_action_group(action_group)
        return ui_manager

    def add_file_menu_actions(self, action_group):
        action_filemenu = gtk.Action("FileMenu", 'Меню', None, None)
        action_group.add_action(action_filemenu)
        action_filequit = gtk.Action("FileQuit", 'Выход', None, gtk.STOCK_QUIT)
        action_group.add_action(action_filequit)
        action_filequit.connect("activate", gtk.main_quit)

    def add_edit_menu_actions(self, action_group):
        action_editmenu = gtk.Action("EditMenu", "Настройки", None, None)
        action_group.add_action(action_editmenu)
        action_about = gtk.Action("SettingsCategories", 'Настройки категорий и слов', None, None)
        action_group.add_action(action_about)

    def add_about_menu_actions(self, action_group):
        action_aboutmenu = gtk.Action("AboutMenu", 'Справка', None, None)
        action_group.add_action(action_aboutmenu)
        action_about = gtk.Action("About", 'О программе', None, gtk.STOCK_ABOUT)
        action_group.add_action(action_about)


if __name__ == '__main__':
    window = Window()
    window.connect("delete-event", gtk.main_quit)
    window.show_all()
    gtk.main()
