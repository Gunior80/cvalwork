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


class MainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_size_request(700, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title('Генератор кроссворда')
        ui_manager = self.create_ui_manager()
        menubar = ui_manager.get_widget("/MenuBar")
        main_box = gtk.VBox()                          # Основной компоновщик
        work_box = gtk.HBox()
        left_box = gtk.VBox()
        buttons_box = gtk.HBox()
        switch_button = gtk.Button('Заполнен/Пустой')
        save_button = gtk.Button('Сохранить')
        right_box = gtk.VBox()
        combo_label = gtk.Label("Категория")
        self.combo = gtk.combo_box_new_text()
        gen_button = gtk.Button('Сгенерировать')
        gen_button.set_size_request(0, 50)
        num_words_label = gtk.Label("Макс. кол-во слов\n по умолчанию 10")
        self.adj = gtk.Adjustment(10, 10, 20, 1, 1, 0)
        num_words = gtk.SpinButton(self.adj,0,0)
        zatychka2 = gtk.Label()

        '''draw'''
        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.set_size_request(200, 200)
        self.drawing_area.show()

        '''pack'''
        buttons_box.pack_start(switch_button)
        buttons_box.pack_start(save_button)
        left_box.pack_start(self.drawing_area)
        left_box.pack_start(buttons_box, expand =False)
        right_box.pack_start(combo_label, expand =False)
        right_box.pack_start(self.combo, expand =False)
        right_box.pack_start(num_words_label, expand =False)
        right_box.pack_start(num_words, expand =False)
        right_box.pack_start(zatychka2, expand = False)
        right_box.pack_start(gen_button, expand =False)
        work_box.pack_start(left_box)
        work_box.pack_start(right_box, expand =False)
        main_box.pack_start(menubar, False, False, 0)
        main_box.pack_start(work_box)
        self.add(main_box)

        self.drawing_area.connect("configure_event", self.configure_event)
        self.drawing_area.connect("expose_event", self.expose_event)
        switch_button.connect("clicked", self.on_switch_button_click)
        save_button.connect("clicked", self.on_save_button_click)
        gen_button.connect("clicked", self.on_gen_button_click)
        self.connect('check-resize', self.redraw)
        self.combo.connect('changed', self.value_changed)

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

    def value_changed(self, combobox):
        '''Переопределяемый метод выбора категории'''
        pass

class SettingsWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_size_request(500, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title('Настройки категорий и слов')
        work_box  = gtk.VBox()

        labels_box = gtk.HBox()
        left_label = gtk.Label('   Список \n категорий')
        right_label = gtk.Label('Список слов\nв категории')
        zatychka = gtk.Label()

        lists_box = gtk.HBox()
        left_box = gtk.VBox()

        scroller_categories = gtk.ScrolledWindow()
        scroller_categories.show()
        self.cat_list = gtk.List()
        scroller_categories.add_with_viewport(self.cat_list)
        self.left_entry = gtk.Entry()
        left_add_rm = gtk.HBox()
        add_cat = gtk.Button('Добавить\nкатегорию')
        rm_cat = gtk.Button('Удалить\nкатегорию')

        right_box = gtk.VBox()

        scroller_words = gtk.ScrolledWindow()
        scroller_words.show()
        self.words_list = gtk.List()
        scroller_words.add_with_viewport(self.words_list)
        self.right_entry = gtk.Entry()
        right_add_rm = gtk.HBox()
        add_word = gtk.Button('Добавить\nслово')
        rm_word = gtk.Button('Удалить\nслово')


        ok_button = gtk.Button('ОК')
        ok_button.set_size_request(30,40)
        
        left_add_rm.pack_start(add_cat)
        left_add_rm.pack_start(rm_cat)

        right_add_rm.pack_start(add_word)
        right_add_rm.pack_start(rm_word)
        
        left_box.pack_start(scroller_categories)
        lists_box.pack_start(left_box)
        left_box.pack_start(self.left_entry, expand = False)
        left_box.pack_start(left_add_rm, expand = False)

        right_box.pack_start(scroller_words)
        lists_box.pack_start(right_box)
        right_box.pack_start(self.right_entry, expand = False)
        right_box.pack_start(right_add_rm, expand = False)

        labels_box.pack_start(left_label)
        labels_box.pack_start(right_label)
        
        work_box.pack_start(labels_box, expand =False)
        work_box.pack_start(lists_box)
        work_box.pack_start(zatychka, expand = False)
        work_box.pack_start(ok_button, False, False)
        self.add(work_box)

        ok_button.connect("clicked", self.on_ok_button_click)
        add_word.connect("clicked", self.on_add_word_click)
        rm_word.connect("clicked", self.on_rm_word_click)
        add_cat.connect("clicked", self.on_add_cat_click)
        rm_cat.connect("clicked", self.on_rm_cat_click)
        self.cat_list.connect("selection_changed", self.on_category_select)
        self.words_list.connect("selection_changed", self.on_word_select)

    def on_ok_button_click(self, event):
        pass
    
    def on_add_word_click(self, event):
        pass

    def on_rm_word_click(self, event):
        pass

    def on_add_cat_click(self, event):
        pass

    def on_rm_cat_click(self, event):
        pass

    def on_category_select(self, gtklist, event, frame):
        pass

    def on_word_select(self, gtklist, event, frame):
        pass

if __name__ == '__main__':
    window = MainWindow()
    window.connect("delete-event", gtk.main_quit)
    window.show_all()
    gtk.main()
