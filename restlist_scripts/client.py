#!/usr/bin/env python3

'''
    REST access library + client example
'''

import json

import requests


HEADERS = {"content-type": "application/json"}


class RestListError(Exception):
    '''Error caused by wrong responses from server'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'RestListError: {self.msg}'


class RestListClient:
    '''Library to access to the REST API of restlist'''
    def __init__(self, uri, timeout=120):
        '''uri should be the root of the API,
            example: http://127.0.0.1:5000/
        '''
        self.root = uri
        if not self.root.endswith('/'):
            self.root = f'{self.root}/'
        self.timeout = timeout

    def append(self, element):
        '''Send request to add an element into the list'''
        if not isinstance(element, str):
            raise ValueError("element must be a string")
        req_body = {"element": element}
        result = requests.put(
            f'{self.root}v1/elements',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestListError(f'Unexpected status code: {result.status_code}')

    def __getitem__(self, index):
        '''Access to a item by its index'''
        if not isinstance(index, int):
            raise ValueError("index must be an integer value")
        result = requests.get(
            f'{self.root}v1/elements/{index}',
            timeout=self.timeout
        )
        if result.status_code == 404:
            raise IndexError("list index out of range")
        if result.status_code != 200:
            raise RestListError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def wipe(self):
        '''Send request to remove all elements from the list'''
        result = requests.delete(
            f'{self.root}v1/elements',
            timeout=self.timeout
        )
        if result.status_code != 204:
            raise RestListError(f'Unexpected status code: {result.status_code}')

    def exists(self, element):
        '''Send request to check if an element exists in the list'''
        if not isinstance(element, str):
            raise ValueError("element is not a string value")
        req_body = {"element": element}
        result = requests.post(
            f'{self.root}v1/elements/exists',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        return result.status_code == 204

    def __contains__(self, element):
        return self.exists(element)

    def remove(self, element, all_occurrences=False):
        '''Send request to remove an element from the list'''
        if not isinstance(element, str):
            raise ValueError("element is not a string value")
        req_body = {"element": element, "remove_all": all_occurrences}
        result = requests.delete(
            f'{self.root}v1/elements',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code == 404:
            raise ValueError(f'Element "{element}" not in the list')
        return result.status_code == 204

    def count(self, element):
        '''Query for number of occurrences of a given item'''
        if not isinstance(element, str):
            raise ValueError("element is not a string value")
        req_body = {"element": element}
        result = requests.post(
            f'{self.root}v1/elements/count',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        response = result.content.decode('utf-8')
        try:
            return int(response)
        except ValueError as error:
            raise RestListError(f'Unknown response from server: {response}') from error

    def len(self):
        '''Send a request to get the number of elements in the list'''
        result = requests.get(
            f'{self.root}v1/elements/count',
            headers=HEADERS,
            timeout=self.timeout
        )
        response = result.content.decode('utf-8')
        try:
            return int(response)
        except ValueError as error:
            raise RestListError(f'Unknown response from server: {response}') from error

    def __len__(self):
        return self.len()


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
