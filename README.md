# Ejemplo de API REST

Demostración para **Python 3** de API REST creando un servidor con Flask y un cliente con requests.

Crear un entorno virtual y activarlo:
```shell
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:
```shell
pip install -r requeriments.txt
```

Podemos lanzar la *test suite* utilizando *Tox*:
```shell
pip install tox
tox
```

Se puede lanzar en un terminal el servidor:
```shell
python3 -m restlist_scripts.server
```

Y en otro el cliente (que ejecuta código de prueba):
```shell
python3 -m restlist_scripts.client
```
Añadiremos el siguiente directorio al PATH:
```shell
export PATH=$(cwd)/.venv/bin:$PATH
```
