from crud import *

# USER NODE
user_properties = {
    "nombre": str,
    "edad": int,
    "email": str,
    "activo": bool,
    "generos_favoritos": list
}

user_data = request_data(user_properties)

create_node(["USUARIO", "GAMER"], **user_data)