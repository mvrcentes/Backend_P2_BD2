import sys
sys.path.insert(0, '/backend/')

from crud import *

user_properties = {
    "nombre": str,
    "edad": int,
    "email": str,
    "activo": bool,
    "generos_favoritos": list
}

# Solicitar datos al usuario
user_data = request_data(user_properties)

# Crear el nodo con los datos proporcionados
create_node(["PERSON", "ACTOR"], **user_data)