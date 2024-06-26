from py2neo import Node, Relationship, NodeMatcher, RelationshipMatcher
from database import *

def create_node(labels, **properties):
    node = Node(*labels, **properties)
    graph.create(node)
    return node

def merge_node(labels, key_property, key_value, **properties):
    matcher = NodeMatcher(graph)
    node = matcher.match(*labels).where(f"_.{key_property} = '{key_value}'").first()
    
    if node:
        # Update existing node properties
        for prop, value in properties.items():
            node[prop] = value
        graph.push(node)
        return False
    else:
        # Create a new node
        node = Node(*labels, **{key_property: key_value, **properties})
        graph.create(node)
        return True

def delete_node(node):
    graph.delete(node)

#Operacion que permita agregar 1 o mas propiedades a un nodo
def add_properties_for_node(matcher, label, property_name, property_value, **properties):
    node = matcher.match(label).where(f"_.{property_name} = '{property_value}'").first()
    for prop, value in properties.items():
        node[prop] = value
    graph.push(node)

 #Operación que permita realizar la actualización de 1 o más propiedades de un nodo
def update_node_properties(label, property_name, property_value, **properties):
    matcher = NodeMatcher(graph)
    node = matcher.match(label).where(f"_.{property_name} = '{property_value}'").first()
    for prop, value in properties.items():
        node[prop] = value
    graph.push(node)

def delete_node_properties(label, property_name, property_value, *properties):
    matcher = NodeMatcher(graph)
    node = matcher.match(label).where(f"_.{property_name} = '{property_value}'").first()
    if node:
        query = (
            f"MATCH (n:{label} {{ {property_name}: '{property_value}' }}) "
            f"REMOVE {', '.join([f'n.{prop}' for prop in properties])}"
        )
        graph.run(query)

def create_relation(start_node, relationship_type, end_node, **properties):
    relation = Relationship(start_node, relationship_type, end_node, **properties)
    graph.create(relation)
    return relation

def merge_relation(start_node, relationship_type, end_node, **properties):
    relation = Relationship(start_node, relationship_type, end_node, **properties)
    graph.merge(relation)
    return relation

def delete_relation(relation):
    graph.separate(relation)

def request_data(properties):
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
                    if prop == "fundacion" or prop == "fecha_lanzamiento" or prop == "fecha_publicacion" or prop == "lanzamiento":
                        user_input = input(f"Enter {prop} (YYYY-MM-DD), leave blank if not applicable: ")
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