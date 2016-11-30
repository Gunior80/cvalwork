#/usr/bin/python
#-*- coding: utf-8 -*-

import gtk, pango

from interface import MainWindow, SettingsWindow
from algorithm import *
from database import *

class Settings(SettingsWindow):
    def __init__(self):
        SettingsWindow.__init__(self)


    def on_ok_button_click(self, event):
        list_cat = get_categories()
        for cat in list_cat:
            Driver().combo.append_text(cat)
        self.hide()

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

class Driver(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
        self.last_gen_list = [[]]
        self.filled = False

        cat_list = get_categories()
        for cat in cat_list:
            self.combo.append_text(cat)


    def on_settings_click(self, event):
        settings = Settings()
        settings.show_all()

    def on_about_click(self, event):
        pass

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
            filter.add_mime_type("image/jpeg")
            filter.add_pattern("*.jpg")
            dialog.add_filter(filter)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                pixbuf.save('path'+'.jpg', "jpeg")
            elif response == gtk.RESPONSE_CANCEL:
                pass
            dialog.destroy()

    def on_gen_button_click(self, event):

        word_list = get_words(self.current_cat)
        for i in word_list:
            print(i)

        a = Generator('-', word_list)
        a.generate_crossword(int(self.adj.get_value()))
        print(len(a.used_words))
        self.last_gen_list = a.grid
        self.draw(self.last_gen_list, self.filled)

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


if __name__ == '__main__':
    window = Driver()
    window.connect("delete-event", gtk.main_quit)
    window.show_all()
    gtk.main()
