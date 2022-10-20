#!/usr/bin/env python3

'''
    Implementacion del servicio de directorios DIRESTORY
'''
import os
import sqlite3
import uuid
import json
import string
from collections import deque

BD_PATH = "./db/data.db"

# class Dir:
#     def __init__(self, parent_id, name, user):
#         self.parent_id = parent_id
#         self.dir_name = name
#         self.child_dir = {}
#         self.child_tuple = []
#         self.readable_by = [user]
#         self.writeable_by = [user]


class Dir_BD:
    '''Implementa todas las operaciones sobre un objeto tipo Dir()'''

    def __init__(self):
        ok=True
        if os.path.exists(BD_PATH):
            try:
                self.bd_con = sqlite3.connect(BD_PATH)
                cur = self.bd_con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS directories(uuid text PRIMARY KEY, uuid_parent text, name text, childs text [], tuples text [], readable_by text [], writeable_by text [])")  
                cur.execute("SELECT * FROM directories")   
                if not cur.fetchone():
                    self.bd_con.commit()
                    self.bd_con.close()
                    self.init_root()
            except Exception as Error:
                print(Error)
        else:
            print("No existe un fichero llamado "+BD_PATH)
            ok=False
        return ok
        
        
    def init_root(self): 
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
   
        id=uuid.uuid1()
        uuid_parent=0
        name="/"
        readable_by = list()
        writeable_by =list()
        readable_by.append("admin")
        writeable_by.append("admin")
        
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)
        
        sql_data=(str(id), uuid_parent, name, readable_by_str, writeable_by_str)
        sql_sentence=("INSERT INTO directories(uuid, uuid_parent, name, readable_by, writeable_by) VALUES(?,?,?,?,?)")
        cur.execute(sql_sentence, sql_data)
       
        self.bd_con.commit()
        self.bd_con.close()
        
       
    def _checkUser_Writeable(self, id_dir, user):

        '''Comprueba si el user esta en writeable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id_dir,)
        sql_sentence = ("SELECT writeable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        writeable_by_tup = cur.fetchone()[0]
        
        writeable_by = json.loads(writeable_by_tup)
        
        self.bd_con.close()
        
        if user not in writeable_by:
            return False

        return True

    def _checkUser_Readable(self, id_dir, user):  
        '''Comprueba si el user esta en writeable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id_dir,)
        sql_sentence = ("SELECT readable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        readable_by_tup = cur.fetchone()[0]
        
        readable_by = json.loads(readable_by_tup)
        
        self.bd_con.close()
        
        if user not in readable_by:
            return False

        return True

    def _get_Name_dir(self, id):
        '''obtener UUID de un dir'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (id,)
        sql_sentence = ("SELECT name FROM directories WHERE uuid=?")
        cur.execute(sql_sentence, sql_data)
        name = cur.fetchone()[0]
                
        self.bd_con.close()
                
        return str(name)


    def _get_UUID_dir(self, uuid_parent, name):
        '''obtener UUID de un dir'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (uuid_parent, name)
        sql_sentence = ("SELECT uuid FROM directories WHERE uuid_parent=? AND name=?")
        cur.execute(sql_sentence, sql_data)
        uuid_dir = cur.fetchone()[0]
                
        self.bd_con.close()
                
        return str(uuid_dir)


    def _get_dirChilds(self, uuid):
        cur = self.bd_con.cursor()
        sql_data = (str(uuid))
        sql_sentence = ("SELECT childs FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        childs_tuple = cur.fetchone()[0]
        return childs_tuple


    def _get_dirFiles(self, uuid):
        cur = self.bd_con.cursor()
        sql_data = (str(uuid))
        sql_sentence = ("SELECT tuples FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        files_tuple = cur.fetchone()[0]
        return files_tuple


    def _get_writeableBy(self, id):
        '''Comprueba si el user esta en writeable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id,)
        sql_sentence = ("SELECT writeable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        writeable_by_tup = cur.fetchone()[0]
        
        writeable_by = json.loads(writeable_by_tup)
        
        self.bd_con.close()
        
        return writeable_by


    def _get_UUID_parent(self, id):
        '''obtener UUID de un dir'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (id,)
        sql_sentence = ("SELECT uuid_parent FROM directories WHERE uuid=?")
        cur.execute(sql_sentence, sql_data)
        uuid_parent = cur.fetchone()[0]
                
        self.bd_con.close()
                
        return str(uuid_parent)
        

    def _get_readableBy(self, id):
        '''Comprueba si el user esta en readable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id,)
        sql_sentence = ("SELECT readable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        readable_by_tup = cur.fetchone()[0] 
        readable_by = json.loads(readable_by_tup)
        
        self.bd_con.close()
        
        return readable_by
    
    
    def _get_dirURL(self, id):
        '''Obtener la el path de un dir desde root'''
        dir_name=self._get_Name_dir(id)
        path = "" 
        listPath = deque()
        listPath.append(dir_name)
        while(dir_name != "/"):
            parent = self._get_UUID_parent(id)
            dir_name = self._get_Name_dir(parent)
            listPath.append(dir_name)
        
        while(listPath.count()!= 0):
            path += listPath.pop() + "/"
        
        return path
        
        
    def create_dir(self, uuid_parent, name, user):
        '''Crea un nuevo directorio incluyendolo en la BD'''
        
        has_permission = self._checkUser_Writeable(uuid_parent, user)
        print(has_permission)
        if not has_permission:
            #throw_exception
            pass
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()

        id=uuid.uuid1()
        readable_by = list()
        writeable_by = list()
        readable_by.append(user)
        writeable_by.append(user)
        
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)

        sql_data=(str(id), uuid_parent, name, readable_by_str, writeable_by_str)
        sql_sentence = ("INSERT INTO directories(uuid, uuid_parent, name, readable_by, writeable_by) VALUES(?,?,?,?,?)")
        
        cur.execute(sql_sentence, sql_data)
        
        self.bd_con.commit()
        
        '''Añade nuevo child al parent'''
        childs = self._get_dirChilds(uuid_parent)
        new_child = str(id)
        childs_list = json.loads(childs) 
            
        childs_list.append(new_child)
        childs_str = json.dumps(childs_list)

        sql_data3 =(childs_str, uuid_parent)
        sql_sentence3  = ("UPDATE directories SET childs=? WHERE uuid=?")
        
        cur.execute(sql_sentence3, sql_data3)
        
        self.bd_con.commit()
        self.bd_con.close()


    def remove_dir(self, uuid_parent, name, user):
        '''Elimina un directorio de la BD'''
        
        id_dir = self._get_UUID_dir(uuid_parent, name)
        has_permission = self._checkUser_Writeable(id_dir, user)
        if not has_permission:
            #throw_exception
            pass
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (id_dir,)
        sql_sentence = ("DELETE FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        
        '''Eliminar este dir de childs del parent'''
        childs = self._get_dirChilds(uuid_parent)   
        childs_list = json.loads(childs)
        childs_list.remove(id_dir)
        childs_str = json.dumps(childs_list)
        
        sql_data3 = (childs_str, uuid_parent,)
        sql_sentence3 = ("UPDATE directories SET childs=? WHERE uuid=?")    

        cur.execute(sql_sentence3, sql_data3)

        self.bd_con.commit()
        self.bd_con.close()
        
        
    def add_user_readable(self, id, user, owner):  
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
            #throw_exception
            pass

        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        readers=self._get_readableBy(id)  
        readers.append(user)
        readers_str=json.dumps(readers)
        
        sql_data=(readers_str, id,)
        sql_sentence=("UPDATE directories SET readable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
                

    def remove_user_readable(self, id, user, owner):  
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Readable(id, owner)
        if not has_permission:
            #throw_exception
            pass

        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        readers=self._get_readableBy(id)  
        readers.remove(user)
        readers_str=json.dumps(readers)
        
        sql_data=(readers_str, id,)
        sql_sentence=("UPDATE directories SET readable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()


    def add_user_writeable(self,id, user, owner):
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
            #throw_exception
            pass

        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        writers=self._get_writeableBy(id)  
        writers.append(user)
        writers_str=json.dumps(writers)
        
        sql_data=(writers_str, id,)
        sql_sentence=("UPDATE directories SET writable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
                

    def remove_user_writeable(self, id, user, owner):
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
            #throw_exception
            pass

        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        writers=self._get_writeableBy(id)  
        writers.remove(user)
        writers_str=json.dumps(writers)
        
        sql_data=(writers_str, id,)
        sql_sentence=("UPDATE directories SET writeable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        
        
    
    def add_file(self, id, user, name, url):
        '''Vacia la lista'''
        has_permission = self._checkUser_Writeable(id, user)
        if not has_permission:
            #throw_exception
            pass    

        file_tuple = (name, url)
        tuples_raw=self._get_dirFiles(id)
        tuples_list = json.loads(tuples_raw)   
        if file_tuple in tuples_list:
            #throws_exception
            pass
        
        childs=self._get_dirChilds(id)
        childs_list = json.loads(childs)
        
        for child in childs_list:
            if name == self._get_Name_dir(child):
                #throw_exception
                pass
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        tuples_list.append(file_tuple)
        tuples_str = json.dumps(tuples_list)
        sql_data = (tuples_str, id,)
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()
    
    
    def remove_file(self, id, user, name, url):
        '''Vacia la lista'''
        has_permission = self._checkUser_Writeable(id, user)
        if not has_permission:
            #throw_exception
            pass    

        file_tuple = (name, url)
        tuples_raw=self._get_dirFiles(id)
        tuples_list = json.loads(tuples_raw)   
        if file_tuple in tuples_list:
            #borrar
            pass
        else:
            #throw_exception
            pass
        
        childs=self._get_dirChilds(id)
        childs_list = json.loads(childs)
        
        for child in childs_list:
            if name == self._get_Name_dir(child):
                #borrar
                pass
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        tuples_list.append(file_tuple)
        tuples_str = json.dumps(tuples_list)
        sql_data = (tuples_str, id,)
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()


if __name__=="__main__":
    dirDB=Dir_BD()
    
    dirDB.create_dir(1, "prueba", "admin")
    #dirDB.remove_dir(1, "prueba", "admin")
