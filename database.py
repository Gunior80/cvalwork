#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

'''
Функции для работы с базой данных SQLlite
'''

def get_categories(): # Получить список пользовательских категорий
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('SELECT name_category FROM categories;')
    data = c.fetchall()
    c.close()
    conn.close()
    return [unicode(i[0]) for i in data]

def get_words(category): # Получить слова из БД
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('SELECT id_category FROM categories WHERE name_category = "%s";' % (category))
    id_cat = c.fetchone()
    c.close()
    c = conn.cursor()
    c.execute('SELECT word FROM words WHERE id_category = %s;' % (id_cat))
    data = c.fetchall()
    c.close()
    conn.close()
    return [unicode(i[0]) for i in data]

def delete_word(category, word): # Удалить слово из категории
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('SELECT id_category FROM categories WHERE name_category = "%s";' % (category))
    id_cat = c.fetchone()
    c.close()
    c = conn.cursor()
    c.execute('DELETE FROM words WHERE id_category = %s AND word = "%s";' % (id_cat[0], word))
    conn.commit()
    c.close()
    conn.close()

def delete_category(category): # Удалить категорию
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    words  = get_words(category)
    for word in words:
        delete_word(category, word)
    c.execute('DELETE FROM categories WHERE name_category = "%s";' % (category))
    conn.commit()
    c.close()
    conn.close()

def set_category(category):
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('INSERT INTO categories(name_category) VALUES("%s");' % (category))
    conn.commit()
    c.close()
    conn.close()

def set_word(category, word): # Занести слово в БД
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('SELECT id_category FROM categories WHERE name_category = "%s";' % category)
    id_cat = c.fetchone()
    c.close()
    avaible_words = get_words(category) 
    if not (word in avaible_words):
        c = conn.cursor()
        c.execute('INSERT INTO words(id_category, word) VALUES(%s, "%s");' % (id_cat[0], word))
        conn.commit()
        c.close()
        conn.close()


    
