#/usr/bin/python
#-*- coding: utf-8 -*-

import gtk

from interface import Window
from algorithm import *

class Driver(Window):
    def on_settings_click(self, event):
        pass

    def on_about_click(self, event):
        pass

    def on_switch_button_click(self, event):
        pass

    def on_save_button_click(self, event):
        pass

    def on_gen_button_click(self, event):
        self.configure_event(self.drawing_area,None)
        x0 = self.null_x
        y0 = self.null_y
        word_list = ['процесс', 'клавиатура', 'поток', 'компилятор',
                     'байткод', 'растр', 'видеокарта', 'регистр', 'ядро', 'ораораропао', 'прмпрпас']

        size = len(word_list) ** 2 - len(word_list)
        a = Generator(size, '-', word_list)
        a.generate_crossword()
        w_l = len(a.grid[0])
        h_l = len(a.grid)
        if w_l > h_l:
            s = self.draw_size/w_l
        else:
            s = self.draw_size/h_l
        print(self.draw_size)
        print(self.null_x)
        print(self.null_y)
        print(s)
        for y1 in range(0, h_l):
            for x1 in range(0, w_l):
                if a.grid[y1][x1] != '-':
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 * s), y0 + (y1 * s), x0 + (x1 + 1) * s, y0 + (y1 * s))
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 * s), y0 + (y1 + 1)* s, x0 + (x1 + 1 ) * s, y0 + (y1 + 1) * s)
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 * s), y0 + (y1 * s), x0 + (x1 * s), y0 + (y1 + 1) * s)
                    self.pixmap.draw_line(self.drawing_area.get_style().black_gc, x0 + (x1 + 1) * s, y0 + (y1 * s), x0 + (x1 + 1) * s, y0 + (y1 + 1) * s)
                    print(x0+(x1*s), y0+(y1*s), x0+(x1+1)*s, y0+(y1+1)*s)
                    self.queue_draw()

if __name__ == '__main__':
    window = Driver()
    window.connect("delete-event", gtk.main_quit)
    window.show_all()
    gtk.main()