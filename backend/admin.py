from crud import *
from nodes_relationships import *

# opcion 1 crear una entidad con merge
def merge_entity(entity_properties, entity_labels):
    # check if property nombre exists
    if "nombre" not in entity_properties:
        entity_value = entity_properties["titulo"]
        entity_key = "titulo"
    else:
        entity_value = entity_properties["nombre"]
        entity_key = "nombre"
    entity_data = request_data(entity_properties)
    merge_node(entity_labels, entity_key, entity_value, **entity_data)

# opcion 2 crear una entidad con create
def create_entity(entity_properties, entity_labels):
    entity_data = request_data(entity_properties)
    create_node(entity_labels, **entity_data)

# opcion 3 actualizar una entidad
def update_entity(entity_properties, entity_labels, entity_type, entity_key):
    entity_name = input(f"Introduzca el nombre de la {entity_type.lower()} que desea actualizar: ")
    entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{entity_name}'").first()
    
    if entity_node:
        entity_data = request_data(entity_properties)
        merge_node(entity_labels, entity_key, entity_name, **entity_data)
    else:
        print(f"{entity_type} no encontrada.")

# opcion 4 eliminar una entidad
def delete_entity(entity_type, entity_key):
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()} que desea eliminar: ")
    entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{entity_name}'").first()
    if entity_node:
        delete_node(entity_node)
    else:
        print("Distribuidora no encontrada.")

# opcion 5 agregar propiedades a una entidad
def add_properties_entity(entity_type, entity_key):
    # pregunta por el nombre de la distribuidora
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()} a la que desea agregar propiedades: ")
    #comprueba si la distribuidora existe
    entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{entity_name}'").first()
    # si la distribuidora existe pregunta por las propiedades a agregar
    if entity_node:
        input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
        properties = dict(item.split(":") for item in input_properties.split(","))
        add_properties_for_node(NodeMatcher(graph), entity_type, entity_key, entity_name, **properties)

# opcion 6 agregar propiedades a multiples entidades
def add_properties_multiple_entities(entity_type, entity_key):
    entity_names = input(f"Introduzca los nombres de {entity_type.lower()} a las que desea agregar propiedades separadas por comas: ")
    entity_names_list = [f"'{name.strip()}'" for name in entity_names.split(",")]

    query = (
        f"MATCH (e:{entity_type}) "
        f"WHERE e.{entity_key} IN [{','.join(entity_names_list)}] "
        "RETURN e"
    )
    entity_nodes = graph.run(query).data()
    # si las distribuidoras existen pregunta por las propiedades a agregar
    if entity_nodes:
        input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
        properties = dict(item.split(":") for item in input_properties.split(","))
        
        for entity_node in entity_nodes:
            add_properties_for_node(NodeMatcher(graph), entity_type, entity_key, entity_node["e"][entity_key], **properties)

# opcion 7 actualizar propiedades de una entidad
def update_properties_entity(entity_type, entity_labels, entity_key):
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()} que desea actualizar: ")
    entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{entity_name}'").first()
    # obtener las propiedades actuales de la distribuidora
    if entity_node:
        current_properties = dict(entity_node)
        print("Propiedades actuales:")
        for key, value in current_properties.items():
            print(f"{key}: {value}")
        # solicitar las propiedades a actualizar
        input_properties = input("Introduzca las propiedades a actualizar en formato clave:valor separadas por comas: ")
        properties = dict(item.split(":") for item in input_properties.split(","))
        # actualizar las propiedades
        update_node_properties(entity_labels, entity_key, entity_name, **properties)

# opcion 8 actualizar propiedades de multiples entidades
def update_properties_multiple(entity_type, entity_labels, entity_key):
    # Solicitar los nombres de las distribuidoras
    entity_names_input = input(f"Introduzca los nombres de {entity_type.lower()} a las que desea actualizar propiedades, separados por comas: ")
    entity_names = [name.strip() for name in entity_names_input.split(",")]

    # Solicitar las propiedades a actualizar
    properties_input = input("Introduzca las propiedades a actualizar en formato clave:valor, separadas por comas: ")
    properties = dict(item.split(":") for item in properties_input.split(","))

    # Para cada distribuidora, actualizar las propiedades especificadas
    for entity_name in entity_names:
        update_node_properties(entity_labels, entity_key, entity_name, **properties)

# opcion 9 eliminar propiedades de una entidad
def delete_properties_entity(entity_type, entity_key):
    # Solicitar el nombre de la distribuidora
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()} a la que desea eliminar propiedades: ")

    # Solicitar las propiedades a eliminar
    properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
    properties = properties_input.split(",")

    # Eliminar las propiedades de la distribuidora
    delete_node_properties(entity_type, entity_key, entity_name, *properties)

# opcion 10 eliminar propiedades de multiples entidades
def delete_properties_multiple(entity_type, entity_key):
    # Solicitar los nombres de las distribuidoras
    entity_names = input(f"Introduzca los nombres de {entity_type.lower()} a las que desea eliminar propiedades, separados por comas: ")
    entity_names_list = [name.strip() for name in entity_names.split(",")]

    # Solicitar las propiedades a eliminar
    properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
    properties = properties_input.split(",")

    # Para cada distribuidora, eliminar las propiedades especificadas
    for entity_name in entity_names_list:
        delete_node_properties(entity_type, entity_key, entity_name, *properties)

# opcion 11 crear relacion utilizando merge
def create_relationship_with_merge(entity_type, entity_key, relation_types):
    start_entity_name = input(f"Introduzca el nombre de la {entity_type} que desea crear la relación: ")
    start_entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{start_entity_name}'").first()
    # si la entidad existe mustra las opciones de relaciones
    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_type = input("Introduzca el tipo de relación: ")
        end_entity_name = input(f"Introduzca el nombre de la {relation_types[relationship_type]['nombre']} con la que desea crear la relación: ")
        # busca si la entidad final existe ustado el enty_key
        end_entity_node = graph.nodes.match(relation_types[relationship_type]["nombre"]).where(f"_.{relation_types[relationship_type]['enty_key']} = '{end_entity_name}'").first()
        # si la entidad final existe crea la relación
        if end_entity_node:
            properties = request_data(relation_types[relationship_type]["propiedades"])
            merge_relation(start_entity_node, relation_types[relationship_type]["tipo_relacion"], end_entity_node, **properties)
        else:
            print(f"{relation_types[relationship_type]['nombre']} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 12 crear relacion utilizando create
def create_relationship_with_create(entity_type, entity_key, relation_types):
    start_entity_name = input(f"Introduzca el nombre de la {entity_type} que desea crear la relación: ")
    start_entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{start_entity_name}'").first()
    # si la entidad existe mustra las opciones de relaciones
    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_type = input("Introduzca el tipo de relación: ")
        end_entity_name = input(f"Introduzca el nombre de la {relation_types[relationship_type]['nombre']} con la que desea crear la relación: ")
        # busca si la entidad final existe ustado el enty_key
        end_entity_node = graph.nodes.match(relation_types[relationship_type]["nombre"]).where(f"_.{relation_types[relationship_type]['enty_key']} = '{end_entity_name}'").first()
        # si la entidad final existe crea la relación
        if end_entity_node:
            properties = request_data(relation_types[relationship_type]["propiedades"])
            create_relation(start_entity_node, relation_types[relationship_type]["tipo_relacion"], end_entity_node, **properties)
        else:
            print(f"{relation_types[relationship_type]['nombre']} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 13 actualizar relacion
def update_relationship(entity_type, entity_key, relation_types):
    start_entity_name = input(f"Introduzca el nombre de la {entity_type} que desea actualizar la relación: ")
    start_entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{start_entity_name}'").first()
    # si la entidad existe mustra las opciones de relaciones
    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_type = input("Introduzca el tipo de relación: ")
        end_entity_name = input(f"Introduzca el nombre de la {relation_types[relationship_type]['nombre']} con la que desea actualizar la relación: ")
        # busca si la entidad final existe ustado el enty_key
        end_entity_node = graph.nodes.match(relation_types[relationship_type]["nombre"]).where(f"_.{relation_types[relationship_type]['enty_key']} = '{end_entity_name}'").first()
        # si la entidad final existe crea la relación
        if end_entity_node:
            properties = request_data(relation_types[relationship_type]["propiedades"])
            merge_relation(start_entity_node, relation_types[relationship_type]["tipo_relacion"], end_entity_node, **properties)
        else:
            print(f"{relation_types[relationship_type]['nombre']} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 14 eliminar relacion
def delete_relationship(entity_type, entity_key, relation_types):
    start_entity_name = input(f"Introduzca el nombre de la {entity_type} que desea eliminar la relación: ")
    start_entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{start_entity_name}'").first()

    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_type = input("Introduzca el tipo de relación: ")
        end_entity_name = input(f"Introduzca el nombre de la {relation_types[relationship_type]['nombre']} con la que desea eliminar la relación: ")
        end_entity_node = graph.nodes.match(relation_types[relationship_type]["nombre"]).where(f"_.{relation_types[relationship_type]['enty_key']} = '{end_entity_name}'").first()
        if end_entity_node:
            relations = list(graph.relationships.match(nodes=(start_entity_node, end_entity_node), r_type=relation_types[relationship_type]["tipo_relacion"]))
            if relations:
                for relation in relations:
                    delete_relation(relation)
                print("Relación(es) eliminada(s) correctamente.")
            else:
                print("Relación no encontrada.")
        else:
            print(f"{relation_types[relationship_type]['nombre']} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 15 agregar propiedades a una relacion
def add_properties_relationship(entity_type, entity_key, relation_types):
    # Solicitar el nombre de la distribuidora
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()}: ")

    # Verificar si la distribuidora existe
    query = (
        f"MATCH (e:{entity_type}) "
        f"WHERE e.{entity_key} = '{entity_name}' "
        "RETURN e"
    )
    start_entity_node = graph.run(query).data()

    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_choice = input("Introduzca el tipo de relación: ")
        relationship_type = relation_types[relationship_choice]["tipo_relacion"]
        end_node_label = relation_types[relationship_choice]["nombre"]
        end_node_key = relation_types[relationship_choice]["enty_key"]

        end_entity_name = input(f"Introduzca el nombre de {end_node_label} con la que desea agregar propiedades a su relación: ")

        query = (
            f"MATCH (e:{end_node_label}) "
            f"WHERE e.{end_node_key} = '{end_entity_name}' "
            "RETURN e"
        )
        end_entity_node = graph.run(query).data()
    
        if end_entity_node:
            input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
            properties = dict(item.split(":") for item in input_properties.split(","))

            query = (
                f"MATCH (:{entity_type} {{{entity_key}: '{entity_name}'}})-[r:{relationship_type}]->(:{end_node_label} {{{end_node_key}: '{end_entity_name}'}}) "
                "SET r += $properties"
            )
            graph.run(query, properties=properties)

# opcion 16 agregar propiedades a multiples relaciones
def add_properties_to_multiple_relationships(entity_type, entity_key, relation_types):
    # Solicitar los nombres de la entidad inicial
    entity_name = input(f"Introduzca el nombre de la {entity_type} a la que desea agregar propiedades de sus relacion: ")
    # Comprueba si la entidad existe
    query = (
        f"MATCH (e:{entity_type}) "
        f"WHERE e.{entity_key} = '{entity_name}' "
        "RETURN e"
    )
    start_entity_node = graph.run(query).data()
    # Si la entidad existe muestra las opciones de relaciones
    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_choice = input("Introduzca el tipo de relación: ")
        relationship_type = relation_types[relationship_choice]["tipo_relacion"]
        end_node_label = relation_types[relationship_choice]["nombre"]
        end_node_key = relation_types[relationship_choice]["enty_key"]

        end_entity_names = input(f"Introduzca los nombres de las {end_node_label} con las que desea agregar propiedades a su relación, separados por comas: ")
        end_entity_names_list = [f"'{name.strip()}'" for name in end_entity_names.split(",")]

        query = (
            f"MATCH (e:{end_node_label}) "
            f"WHERE e.{end_node_key} IN [{','.join(end_entity_names_list)}] "
            "RETURN e"
        )
        end_entity_nodes = graph.run(query).data()

        if end_entity_nodes:
            input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
            properties = dict(item.split(":") for item in input_properties.split(","))
            for end_entity_node in end_entity_nodes:
                node = end_entity_node['e']
                node_name = node['nombre']
                query = (
                    f"MATCH (e:{entity_type} {{{entity_key}: '{entity_name}'}})-[r:{relationship_type}]->"
                    f"(n:{end_node_label} {{{end_node_key}: '{node_name}'}}) "
                    "SET r += $properties"
                )   
                graph.run(query, properties=properties)
        else:
            print(f"{end_node_label} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 17 actualizar propiedades de una relacion
def update_properties_for_relationship(entity_type, entity_key, relation_types):
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()}: ")

    query = (
        f"MATCH (e:{entity_type}) "
        f"WHERE e.{entity_key} = '{entity_name}' "
        "RETURN e"
    )
    start_entity_node = graph.run(query).data()

    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_choice = input("Seleccione el tipo de relación para actualizar propiedades: ")
        relationship_type = relation_types[relationship_choice]["tipo_relacion"]
        end_node_label = relation_types[relationship_choice]["nombre"]
        end_node_key = relation_types[relationship_choice]["enty_key"]

        end_entity_name = input(f"Introduzca el nombre de {end_node_label} cuya relación desea actualizar: ")

        query = (
            f"MATCH (s:{entity_type})-[r:{relationship_type}]->(e:{end_node_label}) "
            f"WHERE s.{entity_key} = '{entity_name}' AND e.{end_node_key} = '{end_entity_name}' "
            "RETURN r, e"
        )
        end_entity_node = graph.run(query).data()

        if end_entity_node and 'r' in end_entity_node[0]:
            print("Propiedades actuales de la relación:")
            relationship_properties = end_entity_node[0]['r']
            for key, value in relationship_properties.items():
                # Convert value to string explicitly to avoid formatting issues
                value_str = str(value)
                print(f"{key}: {value_str}")
            input_properties = input("Introduzca las propiedades a actualizar en formato clave:valor, separadas por comas: ")
            properties = dict(item.split(":") for item in input_properties.split(","))

            query = (
                f"MATCH (s:{entity_type} {{{entity_key}: '{entity_name}'}})-[r:{relationship_type}]->(e:{end_node_label} {{{end_node_key}: '{end_entity_name}'}}) "
                "SET r += $properties"
            )
            graph.run(query, properties=properties)
        else:
            print("No se encontró una relación válida o la entidad especificada.")
    else:
        print(f"No se encontró ninguna entidad con el nombre {entity_name} del tipo {entity_type}.")

# opcion 18 actualizar propiedades de multiples relaciones
def update_properties_to_multiple_relationships(entity_type, entity_key, relation_types):
    entity_name = input(f"Introduzca el nombre de la {entity_type} a la que desea actualizar propiedades de sus relaciones: ")
    query = (
        f"MATCH (e:{entity_type}) "
        f"WHERE e.{entity_key} = '{entity_name}' "
        "RETURN e"
    )
    start_entity_node = graph.run(query).data()

    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_choice = input("Introduzca el tipo de relación: ")
        relationship_type = relation_types[relationship_choice]["tipo_relacion"]
        end_node_label = relation_types[relationship_choice]["nombre"]
        end_node_key = relation_types[relationship_choice]["enty_key"]

        end_entity_names = input(f"Introduzca los nombres de las {end_node_label} con las que desea actualizar propiedades a su relación, separados por comas: ")
        end_entity_names_list = [f"'{name.strip()}'" for name in end_entity_names.split(",")]

        query = (
            f"MATCH (e:{entity_type})-[r:{relationship_type}]->(n:{end_node_label}) "
            f"WHERE e.{entity_key} = '{entity_name}' AND n.{end_node_key} IN [{','.join(end_entity_names_list)}] "
            "RETURN n, r"
        )
        relationships = graph.run(query).data()

        if relationships:
            for i, rel in enumerate(relationships, start=1):
                node = rel['n']
                relationship = rel['r']
                print(f"Propiedades actuales de la relación {i}:")
                if relationship:
                    for key, value in relationship.items():
                        # Convert value to string using str() or custom handling if it's a specific type
                        safe_value = value if isinstance(value, (int, float, str)) else str(value)
                        print(f"{key}: {safe_value}")
                else:
                    print("Esta relación no tiene propiedades definidas.")

                input_properties = input("Introduzca las propiedades a actualizar en formato clave:valor separadas por comas: ")
                properties = dict(item.split(":") for item in input_properties.split(","))

                node_name = node[end_node_key]
                query = (
                    f"MATCH (e:{entity_type} {{{entity_key}: '{entity_name}'}})-[r:{relationship_type}]->"
                    f"(n:{end_node_label} {{{end_node_key}: '{node_name}'}}) "
                    "SET r += $properties"
                )   
                graph.run(query, properties=properties)
        else:
            print(f"No se encontraron relaciones válidas para actualizar.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 19 eliminar 1 o mas propiedades de una relacion
def delete_relationship_properties(entity_type, entity_key, relation_types):
    start_entity_name = input(f"Introduzca el nombre de la {entity_type} a la que desea eliminar propiedades de su relación: ")
    start_entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{start_entity_name}'").first()
    # si la entidad existe mustra las opciones de relaciones
    if start_entity_node:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_type = input("Introduzca el tipo de relación: ")
        end_entity_name = input(f"Introduzca el nombre de la {relation_types[relationship_type]['nombre']} con la que desea eliminar propiedades de su relación: ")
        end_entity_node = graph.nodes.match(relation_types[relationship_type]["nombre"]).where(f"_.{relation_types[relationship_type]['enty_key']} = '{end_entity_name}'").first()
        if end_entity_node:
            # Solicitar las propiedades a eliminar
            properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
            properties = properties_input.split(",")
            # Eliminar las propiedades de la relación
            delete_relation_properties(RelationshipMatcher(graph), entity_type, entity_key, start_entity_name, relation_types[relationship_type]["tipo_relacion"], relation_types[relationship_type]["nombre"], relation_types[relationship_type]["enty_key"], end_entity_name, *properties)
        else:
            print(f"{relation_types[relationship_type]['nombre']} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 20 eliminar 1 o mas propiedades de multiples relaciones
def delete_properties_for_multiple_relationships(entity_type, entity_key, relation_types):
    start_entity_names = input(f"Introduzca los nombres de las {entity_type} a las que desea eliminar propiedades de sus relaciones, separados por comas: ")
    start_entity_names_list = [f"'{name.strip()}'" for name in start_entity_names.split(",")]

    query = (
        f"MATCH (e:{entity_type}) "
        f"WHERE e.{entity_key} IN [{','.join(start_entity_names_list)}] "
        "RETURN e"
    )
    start_entity_nodes = graph.run(query).data()
    if start_entity_nodes:
        print("Tipos de relación disponibles:")
        for relation_name in relation_types:
            print(relation_name)
        relationship_type = input("Introduzca el tipo de relación: ")
        end_entity_name = input(f"Introduzca el nombre de la {relation_types[relationship_type]['nombre']} con la que desea eliminar propiedades de su relación: ")
        end_entity_node = graph.nodes.match(relation_types[relationship_type]["nombre"]).where(f"_.{relation_types[relationship_type]['enty_key']} = '{end_entity_name}'").first()
        if end_entity_node:
            # Solicitar las propiedades a eliminar
            properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
            properties = properties_input.split(",")
            for start_entity_node in start_entity_nodes:
                delete_relation_properties(RelationshipMatcher(graph), entity_type, entity_key, start_entity_node["e"][entity_key], relation_types[relationship_type]["tipo_relacion"], relation_types[relationship_type]["nombre"], relation_types[relationship_type]["enty_key"], end_entity_name, *properties)
        else:
            print(f"{relation_types[relationship_type]['nombre']} no encontrada.")
    else:
        print(f"{entity_type} no encontrada.")

# opcion 19 ver entidades
def show_entities(entity_type):
    query = f"MATCH (n:{entity_type}) RETURN n"
    entities = graph.run(query).data()
    for entity in entities:
        print(entity["n"])
       
def is_operation_applicable(entity_type):
    non_applicable_entities = {
        "GENERO": "No aplicable para géneros debido al modelo de datos",
        "GUIA": "No aplicable para guías debido al modelo de datos",
        "PLATAFORMA": "No aplicable para plataformas debido al modelo de datos",
        "REVIEW": "No aplicable para reseñas debido al modelo de datos"
    }
    
    if entity_type in non_applicable_entities:
        print(non_applicable_entities[entity_type])
        return False
    return True

def menu_modify(menu_type):
    entity_type = menu_type.upper()
    if entity_type == "JUEGO":
        entity_key = "titulo"
        entity_labels = ["JUEGO", "VIDEOJUEGO"]
        entity_properties = {
            "titulo": str,
            "precio": float,
            "lanzamiento": str,
            "plataformas": list
        }
        relation_types = {
            "pertenece_a_genero": {
                "tipo_relacion": "PERTENECE_A",
                "propiedades": {
                    "fecha de lanzamiento": str,
                    "exclusivo": bool,
                    "calificacion_media": int
                },
                "nombre": "GENERO",
                "enty_key": "nombre"
            },
            "tiene_guia": {
                "tipo_relacion": "TIENE",
                "propiedades": {
                    "fecha de creación": str,
                    "autor": str,
                    "disponibilidad": bool
                },
                "nombre": "GUIA",
                "enty_key": "titulo"
            },
            "disponible_en_plataforma": {
                "tipo_relacion": "DISPONIBLE_EN",
                "propiedades": {
                    "formato fisico": str,
                    "formato digital": bool,
                    "edicionespecial": bool
                },
                "nombre": "PLATAFORMA",
                "enty_key": "nombre"
            }
        }     
    elif entity_type == "REVIEW":
        entity_key = "titulo"
        entity_labels = ["REVIEW", "CRITICA"]
        entity_properties = {
            "titulo": str,
            "contenido": str,
            "calificacion": int,
            "fecha": str,
            "util": bool
        }
        relation_types = {
            "califica_a_juego": {
                "tipo_relacion": "CALIFICA",
                "propiedades": {
                    "fecha": str,
                    "importancia": str,
                    "verificado": bool,
                },
                "nombre": "JUEGO",
                "enty_key": "titulo"
            },
            "califica_a_plataforma": {
                "tipo_relacion": "CALIFICA",
                "propiedades": {
                    "fecha": str,
                    "importancia": str,
                    "verificado": bool,
                },
                "nombre": "PLATAFORMA",
                "enty_key": "nombre"
            },
            "califica_a_genero": {
                "tipo_relacion": "CALIFICA",
                "propiedades": {
                    "fecha": str,
                    "importancia": str,
                    "verificado": bool,
                },
                "nombre": "GENERO",
                "enty_key": "nombre"
            },
            "califica_a_distribuidora": {
                "tipo_relacion": "CALIFICA",
                "propiedades": {
                    "fecha": str,
                    "importancia": str,
                    "verificado": bool,
                },
                "nombre": "DISTRIBUIDORA",
                "enty_key": "nombre"
            }  
        }
    elif entity_type == "DISTRIBUIDORA":
        entity_key = "nombre"
        entity_labels = ["DISTRIBUIDORA"]
        entity_properties = {
            "nombre": str,
            "fundacion": str,
            "pais": str,
            "sitio_web": str
        }
        relation_types = {
            "distribuye_juego": {
                "tipo_relacion": "DISTRIBUYE",
                "propiedades": {
                    "fecha_de_lanzamiento": str,
                    "territorios_de distribucion": list,
                    "cantidad_distribuida": int,
                },
                "nombre": "JUEGO",
                "enty_key": "titulo"
            }
        }
    elif entity_type == "GENERO":
        entity_key = "nombre"
        entity_labels = ["GENERO"]
        entity_properties = {
            "nombre": str,
            "popularidad": int,
            "descripcion": str,
            "promedio_calificacion": float
        }
    elif entity_type == "GUIA":
        entity_key = "titulo"
        entity_labels = ["GUIA"]
        entity_properties = {
            "titulo": str,
            "contenido": str,
            "autor": str,
            "fecha_publicacion": str,
            "etiquetas": list
        }
    elif entity_type == "PLATAFORMA":
        entity_key = "nombre"
        entity_labels = ["PLATAFORMA"]
        entity_properties = {
            "nombre": str,
            "fabricante": str,
            "fecha_lanzamiento": str,
            "disponible": bool,
            "exclusivos": list
        }    
    else:
        print("Tipo de entidad no válido.")
        return

    while True:
        print(f"\nMenú de {menu_type}:")
        print("1. Crear {} por medio de la operacion merge".format(entity_type))
        print("2. Crear {} por medio de la operacion create\n".format(entity_type))
        print("3. Actualizar {}".format(entity_type))
        print("4. Eliminar {}\n".format(entity_type))
        print("5. Agregar 1 o mas propiedades a una {}".format(entity_type))
        print("6. Agregar 1 o mas propiedades a multiples {}\n".format(entity_type))
        print("7. Actualizar 1 o más propiedades de un {}".format(entity_type))
        print("8. Actualizar 1 o más propiedades de múltiples {}\n".format(entity_type))
        print("9. Eliminar 1 o mas propiedades de una {}".format(entity_type))
        print("10. Eliminar 1 o mas propiedades de multiples {}\n".format(entity_type))
        print("11. Crear una relacion de una {} por medio de la operacion merge".format(entity_type))
        print("12. Crear una relacion entre una {} por medio de la operacion create\n".format(entity_type))
        print("13. Acctualizar una relacion de una {}".format(entity_type))
        print("14. Eliminar una relacion de una {}\n".format(entity_type))
        print("15. Agregar 1 o mas propiedades a una relacion de la {}".format(entity_type))
        print("16. Agregar 1 o mas propiedades a multiples relaciones de la {}\n".format(entity_type))
        print("17. Actualizar 1 o más propiedades de una relacion de la {}".format(entity_type))
        print("18. Actualizar 1 o más propiedades de múltiples relaciones de la {}\n".format(entity_type))
        print("19. Eliminar 1 o mas propiedades de una relacion de la {}".format(entity_type))
        print("20. Eliminar 1 o mas propiedades de multiples relaciones de la {}\n".format(entity_type))
        print("21. Ver {}".format(entity_type))
        print("22. Regresar")

        choice = input("Por favor, seleccione una opción: ")

        if choice == "1":
            merge_entity(entity_properties, entity_labels)
        elif choice == "2":
            create_entity(entity_properties, entity_labels)
        elif choice == "3":
            update_entity(entity_properties, entity_labels, entity_type)
        elif choice == "4":
            delete_entity(entity_type, entity_key)
        elif choice == "5":
            add_properties_entity(entity_type, entity_key)
        elif choice == "6":
            add_properties_multiple_entities(entity_type, entity_key)
            pass
        elif choice == "7":
            update_properties_entity(entity_type, entity_labels, entity_key)
            pass
        elif choice == "8":
            update_properties_multiple(entity_type, entity_labels, entity_key)
            pass
        elif choice == "9":
            delete_properties_entity(entity_type, entity_key)
            pass
        elif choice == "10":
            delete_properties_multiple(entity_type, entity_key)
            pass
        elif choice == "11":
            if is_operation_applicable(entity_type):
                create_relationship_with_merge(entity_type, entity_key, relation_types)
            pass
        elif choice == "12":
            if is_operation_applicable(entity_type):
                create_relationship_with_create(entity_type, entity_key, relation_types)
            pass
        elif choice == "13":
            if is_operation_applicable(entity_type):
                update_relationship(entity_type, entity_key,relation_types)
            pass
        elif choice == "14":
            if is_operation_applicable(entity_type):
                delete_relationship(entity_type, entity_key, relation_types)
            pass
        elif choice == "15":
            if is_operation_applicable(entity_type):
                add_properties_relationship(entity_type, entity_key, relation_types)
            pass
        elif choice == "16":
            if is_operation_applicable(entity_type):
                add_properties_to_multiple_relationships(entity_type, entity_key, relation_types)
            pass
        elif choice == "17":
            if is_operation_applicable(entity_type):
                update_properties_for_relationship(entity_type, entity_key, relation_types)
            pass
        elif choice == "18":
            if is_operation_applicable(entity_type):
                update_properties_to_multiple_relationships(entity_type, entity_key, relation_types)
            pass
        elif choice == "19":
            if is_operation_applicable(entity_type):
                delete_relationship_properties(entity_type, entity_key, relation_types)
            pass
        elif choice == "20":
            # Placeholder for delete_properties_from_multiple_relationships
            if is_operation_applicable(entity_type):
                delete_properties_for_multiple_relationships(entity_type, entity_key, relation_types)
            pass
        elif choice == "21":
            show_entities(entity_type)
            pass
        elif choice == "22":
            return
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


def admin_menu():
    menu_choices = {
        "1": "DISTRIBUIDORA",
        "2": "JUEGO",
        "3": "GUIA",
        "4": "USUARIO",
        "5": "PLATAFORMA",
        "6": "REVIEW",
        "7": "GENERO",
        "8": "salir"
    }
    
    while True:
        print("\nMenú de Administrador:")
        print("1. Menú de Distribuidora")
        print("2. Menú de Juegos")
        print("3. Menú de Guia de Juegos")
        print("4. Menú de Usuarios")
        print("5. Menú de Plataformas")
        print("6. Menú de Reseñas")
        print("7. Menú de Géneros")
        print("8. Salir")
        
        choice = input("Por favor, seleccione una opción: ")
        
        if choice in menu_choices:
            if menu_choices[choice] == "salir":
                print("Saliendo del sistema.")
                return
            else:
                menu_modify(menu_choices[choice])
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")