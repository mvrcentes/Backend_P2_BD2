from py2neo import Node, Relationship
from database import *

def create_node(labels, **properties):
    node = Node(*labels, **properties)
    graph.create(node)
    return node

def create_relation(start_node, relationship_type, end_node, **properties):
    relation = Relationship(start_node, relationship_type, end_node, **properties)
    graph.create(relation)
    return relation

def merge_node(labels, **properties):
    node = Node(*labels, **properties)
    graph.merge(node)
    return node

def merge_relation(start_node, relationship_type, end_node, **properties):
    relation = Relationship(start_node, relationship_type, end_node, **properties)
    graph.merge(relation)
    return relation

def delete_node(node):
    graph.delete(node)

def delete_relation(relation):
    graph.delete(relation)

def request_data(properties):
    """
    Solicita al usuario que introduzca valores para una serie de propiedades definidas en un diccionario con tipos.
    La función valida los tipos de datos y maneja valores opcionales, repitiendo la solicitud hasta que la entrada sea válida.
    
    :param properties: Un diccionario donde las claves son nombres de propiedades y los valores son los tipos de datos esperados.
    :return: Un diccionario con los valores introducidos y convertidos según los tipos especificados.
    """
    data = {}
    for prop, datatype in properties.items():
        while True:
            try:
                if datatype == list:
                    user_input = input(f"Enter {prop} (separated by comma, e.g., RPG,FPS,MOBA), leave blank if not applicable: ")
                    if user_input == "":
                        data[prop] = []
                    else:
                        data[prop] = [item.strip() for item in user_input.split(',')]
                    break
                elif datatype == bool:
                    user_input = input(f"Enter {prop} (Booleano, e.g., yes or no), leave blank if not applicable: ")
                    if user_input.lower() in ['yes', 'true', '1']:
                        data[prop] = True
                        break
                    elif user_input.lower() in ['no', 'false', '0', '']:
                        data[prop] = False
                        break
                    else:
                        raise ValueError("Please enter 'yes' or 'no'.")
                else:
                    user_input = input(f"Enter {prop} ({datatype.__name__}), leave blank if not applicable: ")
                    if user_input == "" and datatype is not bool:
                        data[prop] = None
                    else:
                        data[prop] = datatype(user_input)
                    break
            except ValueError as e:
                print(f"Invalid input for {prop}, expected {datatype.__name__}. Error: {e}. Please try again.")
    return data

def find_games_by_genre(genre):
    query = (
        "MATCH (g:JUEGO)-[:PERTENECE_A]->(genre:GENERO {nombre: $genre}) "
        'RETURN g.titulo AS Titulo, g.plataformas AS Plataformas, g.lanzamiento AS Fecha_de_Lanzamiento'
    )
    result = graph.run(query, genre=genre)
    return result

def recommend_games_for_user(user_id):
    query = (
        "MATCH (u:GAMER {nombre: $user_id})-[:JUEGA]->(g:JUEGO)<-[:JUEGA]-(other:GAMER)-[:JUEGA]->(rec:JUEGO) "
        "WHERE NOT (u)-[:JUEGA]->(rec) "
        "RETURN rec.titulo AS title, rec.plataformas AS platform, rec.lanzamiento AS release_date, COUNT(*) AS score "
        "ORDER BY score DESC LIMIT 10"
    )
    result = graph.run(query, user_id=user_id)
    return result

def create_user():
    user_properties = {
        "nombre": str,
        "edad": int,
        "email": str,
        "activo": bool,
        "generos_favoritos": list
    }
    user_data = request_data(user_properties)
    return create_node(["USUARIO", "GAMER"], **user_data)

def create_video_game():
    video_game_properties = {
        "titulo": str,
        "precio": float,
        "lanzamiento": str,  
        "plataformas": list
    }
    video_game_data = request_data(video_game_properties)
    return create_node(["VIDEOJUEGO", "JUEGO"], **video_game_data)

def create_genre():
    genre_properties = {
        "nombre": str,
        "popularidad": int,
        "descripcion": str,
        "promedio_calificacion": float
    }
    genre_data = request_data(genre_properties)
    return create_node(["GENERO"], **genre_data)

def create_review():
    review_properties = {
        "titulo": str,
        "contenido": str,
        "calificacion": int,
        "fecha": str,  
        "util": bool
    }
    review_data = request_data(review_properties)
    return create_node(["REVIEW", "CRITICA"], **review_data)

def create_platform():
    platform_properties = {
        "nombre": str,
        "fabricante": str,
        "fecha_lanzamiento": str,  
        "disponible": bool,
        "exclusivos": list
    }
    platform_data = request_data(platform_properties)
    return create_node(["PLATAFORMA"], **platform_data)

def create_publisher():
    publisher_properties = {
        "nombre": str,
        "fundacion": str,  
        "pais": str,
        "sitio_web": str
    }
    publisher_data = request_data(publisher_properties)
    return create_node(["DISTRIBUIDORA"], **publisher_data)

def create_guide():
    guide_properties = {
        "titulo": str,
        "contenido": str,
        "autor": str,
        "fecha_publicacion": str,  
        "etiquetas": list
    }
    guide_data = request_data(guide_properties)
    return create_node(["GUIA"], **guide_data)