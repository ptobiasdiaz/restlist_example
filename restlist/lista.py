#!/usr/bin/env python3

'''
    Implementacion del servicio de directorios DIRESTORY
'''

class Dir_BD:
    '''Implementa todas las operaciones sobre un objeto tipo Dir_BD()'''

    def __init__(self):
        self.storage = []

    def create_dir(self, element):
        '''Incluye un nuevo elemento al final de la lista'''
        self.storage.append(element)

    def remove_dir(self, index):
        '''Retorna el elemento en la posicion "index" de la lista'''
        return self.storage[index]

    def add_user_readable(self, element):
        '''Retorna si un elemento dado esta o no en la lista'''
        return element in self.storage

    def remove_user_readable(self, element, all_occurrences=False):
        '''Elimina un elemento de la lista. Puede eliminar todas sus apariciones'''
        self.storage.remove(element)
        while (element in self.storage) and all_occurrences:
            self.storage.remove(element)

    def add_user_writeable(self, element):
        '''Cuenta el numero de veces que aparece un elemento en la lista'''
        return self.storage.count(element)

    def remove_user_writeable(self):
        '''Devuelve la longitud de la lista'''
        return len(self.storage)

    def add_dir(self):
        '''Vacia la lista'''
        self.storage = []

    def remove_dir(self):
        
