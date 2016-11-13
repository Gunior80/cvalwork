# /usr/bin/env python
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
        #self.set_size_request(500, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        ui_manager = self.create_ui_manager()
        menubar = ui_manager.get_widget("/MenuBar")
        main_box = gtk.VBox()                          # Основной компоновщик
        work_box = gtk.HBox()
        left_box = gtk.VBox()
        buttons_box = gtk.HBox()
        switch_button = gtk.Button('Заполнен/Пустой')
        save_button = gtk.Button('Сохранить')
        rigth_box = gtk.VBox()
        gen_button = gtk.Button('Сгенерировать')

        '''draw'''
        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.set_size_request(200, 200)
        self.drawing_area.show()

        '''upackovka'''
        left_box.pack_start(self.drawing_area)
        left_box.pack_start(buttons_box)
        buttons_box.pack_start(switch_button)
        buttons_box.pack_start(save_button)
        rigth_box.pack_start(gen_button)
        work_box.pack_start(left_box)
        work_box.pack_start(rigth_box)
        main_box.pack_start(menubar, False, False, 0)
        main_box.pack_start(work_box)
        self.add(main_box)

        self.drawing_area.connect("configure_event", self.configure_event)
        self.drawing_area.connect("expose_event", self.expose_event)
        switch_button.connect("clicked", self.on_switch_button_click)
        save_button.connect("clicked", self.on_save_button_click)
        gen_button.connect("clicked", self.on_gen_button_click)

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
        action_filequit = gtk.Action("FileQuit", 'Выход', None, self.on_exit_click)
        action_group.add_action(action_filequit)
        action_filequit.connect("activate", gtk.main_quit)

    def add_edit_menu_actions(self, action_group):
        action_editmenu = gtk.Action("EditMenu", "Настройки", None, None)
        action_group.add_action(action_editmenu)
        action_settings_category = gtk.Action("SettingsCategories", 'Настройки категорий и слов', None, None)
        action_group.add_action(action_settings_category)
        action_settings_category.connect("activate", self.on_settings_click)

    def add_about_menu_actions(self, action_group):
        action_aboutmenu = gtk.Action("AboutMenu", 'Справка', None, None)
        action_group.add_action(action_aboutmenu)
        action_about = gtk.Action("About", 'О программе', None, gtk.STOCK_ABOUT)
        action_group.add_action(action_about)
        action_about.connect("activate", self.on_about_click)

    def configure_event(self, widget, event):
        win = widget.window
        width, height = win.get_size()

        self.pixmap = gtk.gdk.Pixmap(win, width, height)
        self.pixmap.draw_rectangle(widget.get_style().white_gc, True,
                              0, 0, width, height)
        return True

    def expose_event(self, widget, event):
        x, y, width, height = event.area
        if width > height:
            self.null_x = (width - height)/2
            self.null_y = y
            self.draw_size = width = height
        else:
            self.null_y = (height - width)/2
            self.null_x = x
            self.draw_size = width = width
        gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
        widget.window.draw_drawable(gc, self.pixmap, self.null_x, self.null_y, self.null_x, self.null_y, width, height)
        return False

    def redraw(self, widget, event):
        pass

    def on_exit_click(self, event):
        '''Метод закрытия программы'''
        gtk.STOCK_QUIT

    def on_settings_click(self,event):
        '''Переопределяемый метод окрытия окна настроек категорий и слов'''
        pass

    def on_about_click(self, event):
        '''Переопределяемый метод окрытия окна о программе'''
        pass

    def on_switch_button_click(self, event):
        '''Переопределяемый метод нажатия кнопки переключения отображения кроссворда'''
        pass

    def on_save_button_click(self, event):
        '''Переопределяемый метод нажатия кнопки сохранения изображения'''
        pass

    def on_gen_button_click(self, event):
        '''Переопределяемый метод нажатия кнопки генерации кроссворда'''
        pass


if __name__ == '__main__':
    window = Window()
    window.connect("delete-event", gtk.main_quit)
    window.show_all()
    gtk.main()