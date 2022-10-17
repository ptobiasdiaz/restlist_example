#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''

from flask import Flask

from restlist.server import routeApp
from restlist.lista import List

def main():
    '''Entry point'''
    app = Flask("restlist")
    routeApp(app, List())
    app.run(debug=True)


if __name__ == '__main__':
    main()
