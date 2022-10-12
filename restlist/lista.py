#!/usr/bin/env python3

'''
    Implementacion del servicio RESTLIST
'''

class List:
    '''Implementa todas las operaciones sobre un objeto tipo List()'''

    def __init__(self):
        self.storage = []

    def append(self, element):
        '''Incluye un nuevo elemento al final de la lista'''
        self.storage.append(element)

    def element_at(self, index):
        '''Retorna el elemento en la posicion "index" de la lista'''
        return self.storage[index]

    def exists(self, element):
        '''Retorna si un elemento dado esta o no en la lista'''
        return element in self.storage

    def remove(self, element, all_occurrences=False):
        '''Elimina un elemento de la lista. Puede eliminar todas sus apariciones'''
        self.storage.remove(element)
        while (element in self.storage) and all_occurrences:
            self.storage.remove(element)

    def count(self, element):
        '''Cuenta el numero de veces que aparece un elemento en la lista'''
        return self.storage.count(element)

    def len(self):
        '''Devuelve la longitud de la lista'''
        return len(self.storage)

    def wipe(self):
        '''Vacia la lista'''
        self.storage = []
