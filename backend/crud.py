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
        "MATCH (g:Game)-[:HAS_GENRE]->(genre:Genre {name: $genre}) "
        "RETURN g.name AS name, g.platform AS platform, g.release_year AS release_year"
    )
    result = graph.run(query, genre=genre)
    return result

def recommend_games_for_user(user_id):
    query = (
        "MATCH (u:User {id: $user_id})-[:LIKES]->(g:Game)<-[:LIKES]-(other:User)-[:LIKES]->(rec:Game) "
        "WHERE NOT (u)-[:LIKES]->(rec) "
        "RETURN rec.name AS name, rec.platform AS platform, rec.release_year AS release_year, COUNT(*) AS score "
        "ORDER BY score DESC LIMIT 10"
    )
    result = graph.run(query, user_id=user_id)
    return result