from py2neo import Node, Relationship
from database import graph

def testTest():
    print("testTest")

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
                    elif user_input.lower() in ['no', 'false', '0', '']:
                        data[prop] = False
                    else:
                        raise ValueError("Please enter 'yes' or 'no'.")
                else:
                    user_input = input(f"Enter {prop} ({datatype._name_}), leave blank if not applicable: ")
                    if user_input == "" and datatype is not bool:
                        data[prop] = None
                    else:
                        data[prop] = datatype(user_input)
                    break
            except ValueError as e:
                print(f"Invalid input for {prop}, expected {datatype._name_}. Error: {e}. Please try again.")
    return data