#!/usr/bin/env python3

'''
    REST access library + client example
'''

from restlist.client import RestListClient


def main():
    '''Entry point'''
    client = RestListClient('http://127.0.0.1:5000/')
    client.wipe()
    ELEMENTO = 'pepe'
    print('Insertamos "juan"')
    client.append('juan')
    print(f'Insertamos "{ELEMENTO}" 3 veces')
    client.append(ELEMENTO)
    client.append(ELEMENTO)
    client.append(ELEMENTO)
    print(f'Elementos "{ELEMENTO}": ', client.count(ELEMENTO))
    print('Longitud de la lista: ', len(client))
    print(f'Eliminamos un elemento "{ELEMENTO}"')
    client.remove(ELEMENTO)
    print(f'Elementos "{ELEMENTO}": ', client.count(ELEMENTO))
    print('Longitud de la lista: ', len(client))
    print(f'Eliminamos todos los elementos "{ELEMENTO}"')
    client.remove(ELEMENTO, all_occurrences=True)
    print(f'Elementos "{ELEMENTO}": ', client.count(ELEMENTO))
    print('Longitud de la lista: ', len(client))
    print(f'Elemento 0 de la lista: {client[0]}')
    try:
        print(f'Elemento 1 de la lista: {client[1]}')
    except IndexError:
        print('No se puede acceder al elemento 1 de la lista')


if __name__ == '__main__':
    main()
