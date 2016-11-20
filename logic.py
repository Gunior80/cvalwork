#/usr/bin/python
#-*- coding: utf-8 -*-

import gtk, pango

from interface import MainWindow, SettingsWindow
from algorithm import *

class Settings(SettingsWindow):
    pass

class Driver(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
        self.last_gen_list = [[]]
        self.filled = False


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
                pixbuf.save('path', "jpeg")
            elif response == gtk.RESPONSE_CANCEL:
                pass
            dialog.destroy()

    def on_gen_button_click(self, event):
        word_list = ['байткод', 'растр', 'видеокарта', 'регистр', 'фывфыы', 'ораораропао', 'прмпрпас',
                     'байткод', 'растр', 'видеокарта', 'регистр', 'апвпавап', 'ораораропао', 'прмпрпас',
                     'байткод', 'растр', 'видеокарта', 'регистр', 'ждфлывжфдлыв', 'ораораропао', 'прмпрпас']

        size = len(word_list) * 10
        a = Generator(size, '-', word_list)
        a.generate_crossword()
        self.last_gen_list = a.grid
        self.draw(self.last_gen_list, self.filled)

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

                        print(pango_layout.get_width())
                        #pango_layout.set_alignment(pango.ALIGN_LEFT)
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