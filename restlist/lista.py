#!/usr/bin/env python3

'''
    Implementacion del servicio de directorios DIRESTORY
'''

import sqlite3
import uuid
import json

BD_PATH = "./db/data.db"

class Dir:
    def __init__(self, parent_id, name, user):
        self.parent_id = parent_id
        self.dir_name = name
        self.child_dir = {}
        self.child_tuple = []
        self.readable_by = [user]
        self.writeable_by = [user]


class Dir_BD:
    '''Implementa todas las operaciones sobre un objeto tipo Dir()'''

    def __init__(self):
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS directories(uuid text PRIMARY KEY, uuid_parent text, name text, childs text, tuple text, readable_by text, writeable_by text)")  
   
        id=uuid.uuid4()
        uuid_parent=0
        name="/"
        readable_by = ["admin"]
        writeable_by= ["admin"]
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)
        
        sql_data=(str(id), uuid_parent, name, readable_by_str, writeable_by_str)
        sql_sentence=("INSERT INTO directories(uuid, uuid_parent, name, readable_by, writeable_by) VALUES(?,?,?,?,?)")
        cur.execute(sql_sentence, sql_data)
       
        self.bd_con.commit()
        self.bd_con.close()
        
        

    def create_dir(self, uuid_parent, name, user):
        '''Incluye un nuevo elemento al final de la lista'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()

        id=uuid.uuid4()
        readable_by = [user]
        writeable_by= [user]
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)

        sql_data=(str(id), uuid_parent, name, readable_by_str, writeable_by_str)
        sql_sentence = ("INSERT INTO directories(uuid, uuid_parent, name, readable_by, writeable_by) VALUES(?,?,?,?,?,?,?)")

        sql_sentence = ("SELECT name FROM directories WHERE uuid =" +uuid_parent)
        name_parent = cur.fetchone()
        url = name_parent+"/"+name

        

        

    def remove_dir(self, id,name,user):
        '''Retorna el elemento en la posicion "index" de la lista'''
        

    def add_user_readable(self, element):
        '''Retorna si un elemento dado esta o no en la lista'''
        

    def remove_user_readable(self, element, all_occurrences=False):
        '''Elimina un elemento de la lista. Puede eliminar todas sus apariciones'''
        

    def add_user_writeable(self, element):
        '''Cuenta el numero de veces que aparece un elemento en la lista'''
        

    def remove_user_writeable(self):
        '''Devuelve la longitud de la lista'''
        

    def add_file(self):
        '''Vacia la lista'''
        

    def remove_file(self):
        pass


if __name__=="__main__":
    dir=Dir_BD()
