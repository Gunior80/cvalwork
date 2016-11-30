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
    c.execute('SELECT id_category FROM categories WHERE name_category = "%s";' % category)
    id_cat = c.fetchone()
    c.close()
    c = conn.cursor()
    c.execute('SELECT word FROM words WHERE id_category = %d;' %(id_cat))
    data = c.fetchall()
    c.close()
    conn.close()
    return [unicode(i[0]) for i in data]

def set_words(category, words=[]): # Занести слова в БД
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('SELECT id_category FROM categories WHERE name_category = ?;', (category))
    data = c.fetchone()
    c.close()
    conn.close() 
    if data:
        conn = sqlite3.connect('dict.db')
        c = conn.cursor()
        avaible_words = get_words(category)
        for i in range(len(words)):
            if not words[i] in avaible_words: 
                c.execute('INSERT INTO users(name_user, password, access_level) VALUES(?, ?, ?);', (login, passw, '0'))
        conn.commit()
        c.close()
        conn.close()
    else:
        c.execute('INSERT INTO categories(name_category) VALUES(?);', (category))
        conn.commit()
        c.close()
        conn.close()
        set_words(category, words)

def delete_word(id_cat, word): # Удалить слово из категории
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('DELETE FROM words WHERE id_category = ? AND word = ?;', (id_cat, word))
    conn.commit()
    c.close()
    conn.close()

def delete_category(category): # Удалить категорию
    conn = sqlite3.connect('dict.db')
    c = conn.cursor()
    c.execute('SELECT id_category FROM categories WHERE name_category = ?;', (category))
    id_cat = c.fetchone()
    words  = get_words(category)
    for word in words:
        delete_word(id_cat, word)
    c.execute('DELETE FROM categories WHERE category = ?;', (category))
    conn.commit()
    c.close()
    conn.close()
    
