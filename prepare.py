#!/usr/bin/env python3

import os
import sqlite3
from itertools import cycle
from inspect import getsourcefile


def createDatabase(path):
    '''Creates empty tables in path. Returns connection and cursor.'''

    con = sqlite3.connect(path)
    cur = con.cursor()

    # Replace templates table
    cur.execute('DROP TABLE IF EXISTS templates')
    cur.execute('CREATE TABLE templates(id INTEGER PRIMARY KEY, template TEXT NOT NULL)')

    # Replace names table
    cur.execute('DROP TABLE IF EXISTS names')
    cur.execute(
        '''CREATE TABLE names(id INTEGER PRIMARY KEY,
                              name TEXT UNIQUE COLLATE NOCASE,
                              template_id REFERENCES templates(id))''')
    
    # Replace extensions table
    cur.execute('DROP TABLE IF EXISTS extensions')
    cur.execute(
        '''CREATE TABLE extensions(id INTEGER PRIMARY KEY,
                                   extension TEXT UNIQUE COLLATE NOCASE,
                                   template_id REFERENCES templates(id))''')

    con.commit()
    cur.close()

    return con


def extractTemplateInfo(file_name):
    ''' Returns a tuple of template (names, extensions).'''

    file_name, file_ext = file_name.split('.', 1)
    names = file_name.split(',')
    exts = file_ext.split('.')

    return (names, exts)


def addTemplate(cursor, template, names, extensions):
    '''Adds a template to the cursor's database.'''

    # Insert template
    if template is not None:
        cursor.execute('INSERT INTO templates(template) VALUES(?)', [template])
        template_id = cursor.lastrowid

    # Insert names
    if names:
        try:
            cursor.executemany(
                'INSERT INTO names(name, template_id) VALUES(?, ?)', 
                zip(names, cycle([template_id])))
        except sqlite3.IntegrityError:
            pass

    # Insert extensions
    if extensions:
        try:
            cursor.executemany(
                'INSERT INTO extensions(extension, template_id) VALUES(?, ?)',
                zip(extensions, cycle([template_id])))
        except sqlite3.IntegrityError:
            pass


def makeTemplates(plates_path, base_path):
    '''Loads code templates from plates_path into database.'''

    # Initialize database
    with createDatabase(base_path) as con:
        cur = con.cursor()

        file_names = os.listdir(plates_path)
        file_names.sort()

        for file_name in file_names:
            template = open(os.path.join(plates_path, file_name)).read()

            names, extensions = extractTemplateInfo(file_name)

            addTemplate(cur, template, names, extensions)

        cur.close()
        con.commit()


def main():
    source_file = os.path.realpath(getsourcefile(lambda:None))

    source_dir = os.path.split(source_file)[0]

    plates_path = os.path.join(source_dir, 'plates')

    dest_path = os.path.join(source_dir, 'boil/plates.db')

    makeTemplates(plates_path, dest_path)


if __name__ == '__main__':
    main()
