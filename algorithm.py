import random


class Word:
    def __init__(self, word=None):
        self.word = word.lower()
        self.length = len(self.word)
        self.vertical = None

    def vector(self):
        if self.vertical:
            return 'По вертикали'
        else:
            return 'По Горизонтали'

class Generator:
    def __init__(self, cols, rows, empty=' ', available_words=[]):
        self.empty = empty
        self.available_words = available_words
        self.used_words = []
        self.sort_word_list()
        self.cols = cols
        self.rows = rows
        self.clear_grid()
        self.generate_crossword()

    def clear_grid(self):
        '''Создать(очистить) Грид(поле кроссворда) и заполнить "пустыми" знаками'''
        self.grid = [[self.empty for j in range(self.cols)] for i in range(self.rows)]

    def sort_word_list(self):  # Сортируем слова по длинне
        temp_list = []
        for word in self.available_words:
            temp_list.append(Word(word))
        temp_list.sort(key=lambda i: len(i.word), reverse=True)  # Сортировать от большего к меньшему.
        self.available_words = temp_list

    def generate_crossword(self):
        self.current_word_list = []
        for word in self.available_words:
            if word not in self.current_word_list:
                self.fill_grid(word)

    def fill_grid(self, word):
        count = 0
        fit = False
        while not fit:
            if len(self.used_words) == 0:
                if word.length < len(self.grid):
                    if random.randint(0,1):
                        self.set_word(self.cols // 2, self.rows // 2 - word.length // 2, True, word, force=True)
                    else:
                        self.set_word(self.cols // 2 - word.length // 2, self.rows // 2, False, word, force=True)
                    fit = True
                else:
                    return
            else:
                coordlist = self.suggest_coord(word)
                try:
                    col, row, vertical = coordlist[count][0], coordlist[count][1], coordlist[count][2]
                except IndexError:
                    return
                if coordlist[count][4]:
                    fit = True
                    self.set_word(col, row, vertical, word, force=True)
            count +=1

    def suggest_coord(self, word):
        coordlist = []
        c_pos = -1                       # Позиция символа в слове (изначально -1)
        for given_char in word.word:     # Перебираем символы слова
            c_pos += 1
            rowc = 0
            for row in self.grid:        # Перебираем строки Грида
                rowc += 1
                colc = 0
                for c in row:            # Перебираем символы в строке Грида
                    colc += 1
                    if given_char == c:  # Если символ найден
                        try:             # Проверка вертикального расположения
                            if rowc - c_pos > 0:  # Проверяем, не выступает ли слово за пределы грида (по минимуму)
                                if ((rowc - c_pos) + word.length) <= self.rows:  # Проверяем, не выступает ли слово за пределы грида (по максимуму)
                                    coordlist.append([colc, rowc - c_pos, 1, colc + (rowc - c_pos), 0])
                        except:
                            pass
                        try:             # Проверка горизонтально расположения
                            if colc - c_pos > 0:  # Проверяем, не выступает ли слово за пределы грида (по минимуму)
                                if ((colc - c_pos) + word.length) <= self.cols:  # Проверяем, не выступает ли слово за пределы грида (по максимуму)
                                    coordlist.append([colc - c_pos, rowc, 0, rowc + (colc - c_pos), 0])
                        except:
                            pass

        new_coordlist = self.sort_coordlist(coordlist, word)
        return new_coordlist

    def sort_coordlist(self, coordlist, word):
        new_coordlist = []
        for coord in coordlist:
            col, row, vertical = coord[0], coord[1], coord[2]
            coord[4] = self.check_fit_score(col, row, vertical, word)
            if coord[4]:
                new_coordlist.append(coord)
        random.shuffle(new_coordlist)
        new_coordlist.sort(key=lambda i: i[4], reverse=True)
        return new_coordlist

    def check_fit_score(self, col, row, vertical, word):
        if col < 1 or row < 1:
            return 0
        count, score = 1, 1
        for letter in word.word:
            try:
                active_cell = self.grid[row - 1][col - 1]
            except IndexError:
                return 0

            if active_cell == self.empty or active_cell == letter:
                pass
            else:
                return 0

            if active_cell == letter:
                score += 1

            if vertical:
                # Проверка возможности вставить слово по вертикали
                if active_cell != letter:  # условие для первой буквы
                    if not self.check_if_cell_clear(col + 1, row):  # Проверка правой позиции
                        return 0

                    if not self.check_if_cell_clear(col - 1, row):  # Проверка левой позиции
                        return 0

                if count == 1:  # Проверка верхней позиции относительно первой буквы
                    if not self.check_if_cell_clear(col, row - 1):
                        return 0

                if count == len(word.word):  # Проверка нижней позиции относительно последней буквы
                    if not self.check_if_cell_clear(col, row + 1):
                        return 0
            else:
                # Проверка возможности вставить слово по горизонтали
                if active_cell != letter:  # условие для первой буквы
                    if not self.check_if_cell_clear(col, row - 1):  # Проверка верхней позиции
                        return 0

                    if not self.check_if_cell_clear(col, row + 1):  # Проверка нижней позиции
                        return 0

                if count == 1:  # Проверка левой позиции относительно первой буквы
                    if not self.check_if_cell_clear(col - 1, row):
                        return 0

                if count == len(word.word):  # Проверка правой позиции относительно последней буквы
                    if not self.check_if_cell_clear(col + 1, row):
                        return 0

            if vertical:
                row += 1
            else:
                col += 1
            count += 1
        return score

    def set_word(self, col, row, vertical, word, force=False):
        # Вставка слова в Грид
        if force:
            word.col = col
            word.row = row
            word.vertical = vertical
            self.used_words.append(word)
            for letter in word.word:
                self.grid[row - 1][col - 1] =  letter
                if vertical:
                    row += 1
                else:
                    col += 1
        return

    def check_if_cell_clear(self, col, row):
        # Проверка незанятости поля
        try:
            cell = self.grid[row - 1][col - 1]
            if cell == self.empty:
                return True
        except IndexError:
            pass
        return False