#!/usr/bin/env python3


from flask import make_response, request

def routeApp(app, LIST):
    '''Enruta la API REST a la webapp'''

    @app.route('/v1/elements', methods=['PUT'])
    def append_element():
        '''Añadir elemento a lista'''
        if not request.is_json:
            return make_response('Missing JSON', 400)
        if 'element' not in request.get_json():
            return make_response('Missing "element" key', 400)
        element = request.get_json()['element']
        LIST.append(element)
        return make_response(element, 200)

    @app.route('/v1/elements', methods=['DELETE'])
    def wipe_or_remove_element():
        '''Borrar un elemento o la lista entera'''
        if not request.is_json:
            LIST.wipe()
            return make_response('', 204)

        if 'element' not in request.get_json():
            return make_response('Missing "element" key', 400)

        remove_all = request.get_json().get('remove_all', False)
        element = request.get_json()['element']
        try:
            LIST.remove(element, all_occurrences=remove_all)
        except ValueError:
            return make_response('Element not found', 404)
        return make_response('', 204)

    @app.route('/v1/elements/<index>', methods=['GET'])
    def element_at(index):
        '''Obtener el elemento numero "index"'''
        try:
            index = int(index)
        except ValueError:
            return make_response("Wrong element index", 400)
        if index not in range(LIST.len()):
            return make_response("Index out of range", 404)
        return make_response(LIST.element_at(index), 200)

    @app.route('/v1/elements/exists', methods=['POST'])
    def element_exist():
        '''Devuelve si un elemento existe en la lista o no'''
        if not request.is_json:
            return make_response('Missing JSON', 400)
        if 'element' not in request.get_json():
            return make_response('Missing "element" key', 400)
        if LIST.exists(request.get_json()['element']):
            return make_response("", 204)
        return make_response("Element not found", 404)

    @app.route('/v1/elements/count', methods=['GET', 'POST'])
    def element_count():
        '''Devuelve la ocurrencias de un elemento en la lista o el tamaño de la lista'''
        if request.method == 'GET':
            return make_response(f"{LIST.len()}", 200)
        if not request.is_json:
            return make_response('Missing JSON', 400)
        if 'element' not in request.get_json():
            return make_response('Missing "element" key', 400)
        element = request.get_json()['element']
        return make_response(f"{LIST.count(element)}", 200)
