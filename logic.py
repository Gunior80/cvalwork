#/usr/bin/python
#-*- coding: utf-8 -*-

import gtk, pango

from interface import MainWindow, SettingsWindow
from algorithm import *
from database import *

class Settings(SettingsWindow):
    list_cat_key   = "list_cat_data"
    list_words_key = "list_words_data"
    def __init__(self, parent=None):
        SettingsWindow.__init__(self)
        self.p = parent
        column = gtk.TreeViewColumn()
        cell = gtk.CellRendererText()
        cats = get_categories()
        self.cat_list.set_model(self.create_model(cats))
        self.cat_list.set_rules_hint(False)
        self.cat_list.append_column(column)
        column.pack_start(cell, False)
        column.add_attribute(cell, 'text', 0)
        self.category = None
        self.word = None

    def on_ok_button_click(self, event):
        self.p.combo_fill()
        self.destroy()

    def on_add_word_click(self, event):
        cat = self.value(self.cat_list.get_selection(), rm = False)
        if cat != None:
            word = self.right_entry.get_text()
            if word != '':
                self.set_value(self.words_list, word)
                set_word(cat, word)
                self.right_entry.set_text('')

    def on_rm_word_click(self, event):
        tree_selection = self.words_list.get_selection()
        del_word = self.value(tree_selection)
        cat = self.value(self.cat_list.get_selection(), rm = False)
        delete_word(cat, del_word)

    def on_add_cat_click(self, event):
        cat = self.left_entry.get_text()
        if cat != '':
            self.set_value(self.cat_list, cat)
            set_category(cat)
            self.left_entry.set_text('')

    def on_rm_cat_click(self, event):
        tree_selection = self.cat_list.get_selection()
        del_cat = self.value(tree_selection)
        if del_cat == self.category:
            self.words_list.get_model().clear()
            self.words_list.remove_column(self.words_list.get_column(0))
        delete_category(del_cat)

    def on_category_select(self, treeview, path, view_column):
        try:
            self.words_list.get_model().clear()
            self.words_list.remove_column(self.words_list.get_column(0))
        except AttributeError:
            pass
        model = treeview.get_model()
        it = model.get_iter(path)
        self.category = model.get_value(it, 0)        
        cats = get_words(self.category)
        if cats == None:
            pass
        else:
            column = gtk.TreeViewColumn()
            cell = gtk.CellRendererText()
            self.words_list.set_model(self.create_model(cats))
            self.words_list.set_rules_hint(True)
            self.words_list.append_column(column)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)

    def value(self, tree_selection,rm = True):
        model, path = tree_selection.get_selected_rows()
        tree_iter = model.get_iter(path[0])
        value = model.get_value(tree_iter,0)
        if rm: model.remove(tree_iter)
        return value
    
    def set_value(self, tree_selection, value):
        model = tree_selection.get_model()
        model.append([value])

    def create_model(self, list = []):
        store = gtk.ListStore(str)
        for item in list:
            store.append([item])
        return store

class Driver(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
        self.last_gen_list = [[]]
        self.filled = False
        self.combo_fill()

    def combo_fill(self):
        try:
            self.combo.clear()
        except:
            pass
        list = get_categories()
        store = gtk.ListStore(str)
        for item in list:
            store.append([item])

        self.combo.set_model(store)
        cell = gtk.CellRendererText()

        self.combo.pack_start(cell)
        self.combo.add_attribute(cell, 'text', 0)


    def on_settings_click(self, event):
        settings = Settings(parent=self)
        settings.show_all()

    def on_about_click(self, event):
        message = gtk.MessageDialog(type=gtk.MESSAGE_INFO)
        ok_button = message.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        ok_button.connect("clicked", lambda x: message.hide())
        message.set_markup("This programm is sucks.")
        message.run()

    def on_switch_button_click(self, event):
        if self.filled == False:
            self.filled = True
        else:
            self.filled = False
        self.draw(self.last_gen_list, self.filled)

    def on_save_button_click(self, event):
        if self.last_gen_list != [[]]:
            width, height = self.pixmap.get_size()

            pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, has_alpha=False, bits_per_sample=8, width=width, height=height)
            pixbuf.get_from_drawable(self.pixmap, self.pixmap.get_colormap(), 0, 0, 0, 0, width, height)
            dialog = gtk.FileChooserDialog(title='Сохранить изображение', action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                            buttons=(
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            filter = gtk.FileFilter()
            filter.set_name("jpeg")
            filter.add_mime_type("image/jpeg")
            filter.add_pattern("*.jpg")
            dialog.add_filter(filter)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                filename = dialog.get_filename()
                if not '.jpg' in filename:
                    filename += '.jpg'
                pixbuf.save(filename, "jpeg")
            elif response == gtk.RESPONSE_CANCEL:
                pass
            dialog.destroy()

    def on_gen_button_click(self, event):
        try:
            word_list = get_words(self.current_cat)
            best = 0
            for i in range(5):
                a = Generator('-', word_list)
                a.generate_crossword(int(self.adj.get_value()))
                if (len(a.used_words) > best):
                    best = len(a.used_words)
                    b = a
                
            b.format_grid()
            self.last_gen_list = b.grid
            self.draw(self.last_gen_list, self.filled)
        except:
            pass

    def clear_model(self, combobox):
        model = combobox.get_model()
        model.clear()

    def value_changed(self, combobox):
        '''Переопределяемый метод выбора категории'''
        model = combobox.get_model()
        index = combobox.get_active()
        if index >= 0:
            self.current_cat = model[index][0]

    def draw(self, list, filled):
        self.configure_event(self.drawing_area, None)
        x0 = self.null_x
        y0 = self.null_y
        w_l = len(list[0])
        h_l = len(list)
        if w_l > h_l:
            s = self.draw_size / w_l
        else:
            s = self.draw_size / h_l
        pango_layout = self.drawing_area.create_pango_layout('')
        fontdesc = pango.FontDescription("Sans " + str(s // 2))
        pango_layout.set_font_description(fontdesc)
        for y1 in range(0, h_l):
            for x1 in range(0, w_l):
                if list[y1][x1] != '-':
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 * s), y0 + (y1 * s),
                                          x0 + (x1 + 1) * s, y0 + (y1 * s))
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 * s), y0 + (y1 + 1) * s,
                                          x0 + (x1 + 1) * s, y0 + (y1 + 1) * s)
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 * s), y0 + (y1 * s),
                                          x0 + (x1 * s), y0 + (y1 + 1) * s)
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 + 1) * s, y0 + (y1 * s),
                                          x0 + (x1 + 1) * s, y0 + (y1 + 1) * s)
                    if self.filled == True:

                        pango_layout.set_text(list[y1][x1])
                        self.pixmap.draw_layout(self.drawing_area.get_style().black_gc, x0 + (x1 * s)+s//3, y0 + (y1 * s), pango_layout)
                    self.queue_draw()

    def redraw(self,s):
        if self.last_gen_list != [[]]:
            self.draw(self.last_gen_list, self.filled)

window = Driver()
window.connect("delete-event", gtk.main_quit)
