from crud import *
from nodes_relationships import *

# opcion 1 crear publisher con merge
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

# opcion 2 crear publisher con create
def create_entity(entity_properties, entity_labels):
    entity_data = request_data(entity_properties)
    create_node(entity_labels, **entity_data)

# opcion 3 actualizar publisher
def update_entity(entity_properties, entity_labels, entity_type, entity_key):
    entity_name = input(f"Introduzca el nombre de la {entity_type.lower()} que desea actualizar: ")
    entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{entity_name}'").first()
    
    if entity_node:
        entity_data = request_data(entity_properties)
        merge_node(entity_labels, entity_key, entity_name, **entity_data)
    else:
        print(f"{entity_type} no encontrada.")

# opcion 4 eliminar publisher
def delete_entity(entity_type, entity_key):
    entity_name = input(f"Introduzca el nombre de {entity_type.lower()} que desea eliminar: ")
    entity_node = graph.nodes.match(entity_type).where(f"_.{entity_key} = '{entity_name}'").first()
    if entity_node:
        delete_node(entity_node)
    else:
        print("Distribuidora no encontrada.")

# opcion 5 agregar propiedades a publisher
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

# opcion 6 agregar propiedades a multiples publishers
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

# opcion 7 actualizar propiedades de un publisher
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

# opcion 8 actualizar propiedades de multiples publishers
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

# opcion 9 eliminar propiedades de un publisher
def delete_properties_from_publisher():
    # Solicitar el nombre de la distribuidora
    publisher_name = input("Introduzca el nombre de la distribuidora a la que desea eliminar propiedades: ")

    # Solicitar las propiedades a eliminar
    properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
    properties = properties_input.split(",")

    # Eliminar las propiedades de la distribuidora
    delete_node_properties("DISTRIBUIDORA", "nombre", publisher_name, *properties)

# opcion 10 eliminar propiedades de multiples publishers
def delete_properties_from_multiple_publishers():
    # Solicitar los nombres de las distribuidoras
    publisher_names_input = input("Introduzca los nombres de las distribuidoras a las que desea eliminar propiedades, separados por comas: ")
    publisher_names = [name.strip() for name in publisher_names_input.split(",")]

    # Solicitar las propiedades a eliminar
    properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
    properties = properties_input.split(",")

    # Para cada distribuidora, eliminar las propiedades especificadas
    for publisher_name in publisher_names:
        delete_node_properties("DISTRIBUIDORA", "nombre", publisher_name, *properties)

# opcion 11 crear relacion entre publisher y juego con merge
def create_publisher_game_relationship_with_merge():
    publisher_id = input("Introduzca el nombre de la distribuidora: ")
    game_id = input("Introduzca el título del juego: ")
    cant_games = int(input("Introduzca la cantidad de juegos distribuidos: "))
    territories = input("Introduzca los territorios de distribución: ")
    fecha_distribucion = input("Introduzca la fecha de distribución: ")
    
    publisher_publishes_game_with_merge(publisher_id, game_id, cant_games, territories, fecha_distribucion)

# opcion 12 crear relacion entre publisher y juego con create
def create_publisher_game_relationship_with_create():
    publisher_id = input("Introduzca el nombre de la distribuidora: ")
    game_id = input("Introduzca el título del juego: ")
    cant_games = int(input("Introduzca la cantidad de juegos distribuidos: "))
    territories = input("Introduzca los territorios de distribución: ")
    fecha_distribucion = input("Introduzca la fecha de distribución: ")
    
    publisher_publishes_game(publisher_id, game_id, cant_games, territories, fecha_distribucion)

# opcion 13 agregar propiedades a una relacion de la distribuidora
def add_properties_to_publisher_relationship():
    publisher_name = input("Introduzca el nombre de la distribuidora a la que desea agregar propiedades a su relación: ")
    publisher_node = graph.nodes.match("DISTRIBUIDORA").where(f"_.nombre = '{publisher_name}'").first()
    if publisher_node:
        relationship_type = input("Introduzca el tipo de relación: ")
        end_node_label = input("Introduzca la etiqueta del nodo final: ")
        end_node_property_name = input("Introduzca el nombre de la propiedad del nodo final: ")
        end_node_property_value = input("Introduzca el valor de la propiedad del nodo final: ")
        input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
        properties = dict(item.split(":") for item in input_properties.split(","))
        add_properties_for_relation(RelationshipMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, relationship_type, end_node_label, end_node_property_name, end_node_property_value, **properties)
    else:
        print("Distribuidora no encontrada.")

# opcion 14 agregar propiedades a multiples relaciones de la distribuidora
def add_properties_to_multiple_publishers():
    # Solicitar los nombres de las distribuidoras
    publisher_names_input = input("Introduzca los nombres de las distribuidoras a las que desea agregar propiedades a sus relaciones, separados por comas: ")
    publisher_names = [name.strip() for name in publisher_names_input.split(",")]

    # Solicitar el tipo de relación
    relationship_type = input("Introduzca el tipo de relación: ")

    # Solicitar la etiqueta del nodo final
    end_node_label = input("Introduzca la etiqueta del nodo final: ")

    # Solicitar el nombre de la propiedad del nodo final
    end_node_property_name = input("Introduzca el nombre de la propiedad del nodo final: ")

    # Solicitar el valor de la propiedad del nodo final
    end_node_property_value = input("Introduzca el valor de la propiedad del nodo final: ")

    # Solicitar las propiedades a agregar
    properties_input = input("Introduzca las propiedades a agregar en formato clave:valor, separadas por comas: ")
    properties = dict(item.split(":") for item in properties_input.split(","))

    # Para cada distribuidora, agregar las propiedades a la relación con el nodo final
    for publisher_name in publisher_names:
        add_properties_for_relation(RelationshipMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, relationship_type, end_node_label, end_node_property_name, end_node_property_value, **properties)

# opcion 15 actualizar propiedades de una relacion de la distribuidora
def update_properties_for_publisher_relationship():
    publisher_name = input("Introduzca el nombre de la distribuidora a la que desea actualizar propiedades de su relación: ")
    publisher_node = graph.nodes.match("DISTRIBUIDORA").where(f"_.nombre = '{publisher_name}'").first()
    # obtener las propiedades actuales de la relación
    if publisher_node:
        relationship_type = input("Introduzca el tipo de relación: ")
        end_node_label = input("Introduzca la etiqueta del nodo final: ")
        end_node_property_name = input("Introduzca el nombre de la propiedad del nodo final: ")
        end_node_property_value = input("Introduzca el valor de la propiedad del nodo final: ")
        relation = graph.match(nodes=(publisher_node, None), r_type=relationship_type, r_nodes=(None, end_node_label)).where(f"_.{end_node_property_name} = '{end_node_property_value}'").first()
        if relation:
            current_properties = dict(relation)
            print("Propiedades actuales:")
            for key, value in current_properties.items():
                print(f"{key}: {value}")
            # solicitar las propiedades a actualizar
            input_properties = input("Introduzca las propiedades a actualizar en formato clave:valor separadas por comas: ")
            properties = dict(item.split(":") for item in input_properties.split(","))
            # actualizar las propiedades
            update_relation_properties(RelationshipMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, relationship_type, end_node_label, end_node_property_name, end_node_property_value, **properties)
        else:
            print("Relación no encontrada.")

# opcion 16 actualizar propiedades de multiples relaciones de la distribuidora
def update_properties_for_multiple_publishers():
    # Solicitar los nombres de las distribuidoras
    publisher_names_input = input("Introduzca los nombres de las distribuidoras a las que desea actualizar propiedades de sus relaciones, separados por comas: ")
    publisher_names = [name.strip() for name in publisher_names_input.split(",")]

    # Solicitar el tipo de relación
    relationship_type = input("Introduzca el tipo de relación: ")

    # Solicitar la etiqueta del nodo final
    end_node_label = input("Introduzca la etiqueta del nodo final: ")

    # Solicitar el nombre de la propiedad del nodo final
    end_node_property_name = input("Introduzca el nombre de la propiedad del nodo final: ")

    # Solicitar el valor de la propiedad del nodo final
    end_node_property_value = input("Introduzca el valor de la propiedad del nodo final: ")

    # Solicitar las propiedades a actualizar
    properties_input = input("Introduzca las propiedades a actualizar en formato clave:valor, separadas por comas: ")
    properties = dict(item.split(":") for item in properties_input.split(","))

    # Para cada distribuidora, actualizar las propiedades de la relación con el nodo final
    for publisher_name in publisher_names:
        update_relation_properties(RelationshipMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, relationship_type, end_node_label, end_node_property_name, end_node_property_value, **properties)


def delete_relation_properties_remove(matcher, start_node_label, start_node_property_name, start_node_property_value, relationship_type, end_node_label, end_node_property_name, end_node_property_value, *properties):   
    start_node = matcher.match(start_node_label).where(f"_.{start_node_property_name} = '{start_node_property_value}'").first()
    end_node = matcher.match(end_node_label).where(f"_.{end_node_property_name} = '{end_node_property_value}'").first()
    relation = Relationship(start_node, relationship_type, end_node)
    query = (
        f"MATCH (n:{start_node_label} {{ {start_node_property_name}: '{start_node_property_value}' }})-[r:{relationship_type}]->(m:{end_node_label} {{ {end_node_property_name}: '{end_node_property_value}' }}) "
        f"REMOVE {', '.join([f'r.{prop}' for prop in properties])}"
    )
    graph.run(query)

# opcion 17 eliminar propiedades de una relacion de la distribuidora
def delete_properties_for_publisher_relationship():
    publisher_name = input("Introduzca el nombre de la distribuidora a la que desea eliminar propiedades de su relación: ")
    publisher_node = graph.nodes.match("DISTRIBUIDORA").where(f"_.nombre = '{publisher_name}'").first()
    # obtener las propiedades actuales de la relación
    if publisher_node:
        relationship_type = input("Introduzca el tipo de relación: ")
        end_node_label = input("Introduzca la etiqueta del nodo final: ")
        end_node_property_name = input("Introduzca el nombre de la propiedad del nodo final: ")
        end_node_property_value = input("Introduzca el valor de la propiedad del nodo final: ")
        properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
        properties = properties_input.split(",")
        delete_relation_properties_remove(RelationshipMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, relationship_type, end_node_label, end_node_property_name, end_node_property_value, *properties)
    else:
        print("Distribuidora no encontrada.")

# opcion 18 eliminar propiedades de multiples relaciones de la distribuidora
def delete_properties_for_multiple_publishers_relationship():
    # Solicitar los nombres de las distribuidoras
    publisher_names_input = input("Introduzca los nombres de las distribuidoras a las que desea eliminar propiedades de sus relaciones, separados por comas: ")
    publisher_names = [name.strip() for name in publisher_names_input.split(",")]

    # Solicitar el tipo de relación
    relationship_type = input("Introduzca el tipo de relación: ")

    # Solicitar la etiqueta del nodo final
    end_node_label = input("Introduzca la etiqueta del nodo final: ")

    # Solicitar el nombre de la propiedad del nodo final
    end_node_property_name = input("Introduzca el nombre de la propiedad del nodo final: ")

    # Solicitar el valor de la propiedad del nodo final
    end_node_property_value = input("Introduzca el valor de la propiedad del nodo final: ")

    # Solicitar las propiedades a eliminar
    properties_input = input("Introduzca las propiedades a eliminar, separadas por comas: ")
    properties = properties_input.split(",")

    # Para cada distribuidora, eliminar las propiedades de la relación con el nodo final
    for publisher_name in publisher_names:
        delete_relation_properties_remove(RelationshipMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, relationship_type, end_node_label, end_node_property_name, end_node_property_value, *properties)

# opcion 19 ver distribuidoras
def show_publishers():
    publishers = graph.nodes.match("DISTRIBUIDORA")
    for publisher in publishers:
        print(dict(publisher))
       

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
    elif entity_type == "GENERO":
        entity_key = "nombre"
        entity_labels = ["GENERO"]
        entity_properties = {
            "nombre": str,
            "popularidad": int,
            "descripcion": str,
            "promedio_calificacion": float
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
    elif entity_type == "DISTRIBUIDORA":
        entity_key = "nombre"
        entity_labels = ["DISTRIBUIDORA"]
        entity_properties = {
            "nombre": str,
            "fundacion": str,
            "pais": str,
            "sitio_web": str
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
    else:
        print("Tipo de entidad no válido.")
        return

    while True:
        print(f"\nMenú de {menu_type}:")
        print("1. Crear {} por medio de la operacion merge".format(entity_type))
        print("2. Crear {} por medio de la operacion create".format(entity_type))
        print("3. Actualizar {}".format(entity_type))
        print("4. Eliminar {}".format(entity_type))
        print("5. Agregar 1 o mas propiedades a una {}".format(entity_type))
        print("6. Agregar 1 o mas propiedades a multiples {}".format(entity_type))
        print("7. Actualizar 1 o más propiedades de un {}".format(entity_type))
        print("8. Actualizar 1 o más propiedades de múltiples {}".format(entity_type))
        print("9. Eliminar 1 o mas propiedades de una {}".format(entity_type))
        print("10. Eliminar 1 o mas propiedades de multiples {}".format(entity_type))
        print("11. Crear una relacion de una {} por medio de la operacion merge".format(entity_type))
        print("12. Crear una relacion entre una {} por medio de la operacion create".format(entity_type))
        print("13. Agregar 1 o mas propiedades a una relacion de la {}".format(entity_type))
        print("14. Agregar 1 o mas propiedades a multiples relaciones de la {}".format(entity_type))
        print("15. Actualizar 1 o más propiedades de una relacion de la {}".format(entity_type))
        print("16. Actualizar 1 o más propiedades de múltiples relaciones de la {}".format(entity_type))
        print("17. Eliminar 1 o mas propiedades de una relacion de la {}".format(entity_type))
        print("18. Eliminar 1 o mas propiedades de multiples relaciones de la {}".format(entity_type))
        print("19. Ver {}".format(entity_type))
        print("20. Regresar")

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
            # Placeholder for add_properties_to_multiple_entities
            pass
        elif choice == "7":
            # Placeholder for update_properties_for_entity
            pass
        elif choice == "8":
            # Placeholder for update_properties_for_multiple_entities
            pass
        elif choice == "9":
            # Placeholder for delete_properties_from_entity
            pass
        elif choice == "10":
            # Placeholder for delete_properties_from_multiple_entities
            pass
        elif choice == "11":
            # Placeholder for create_relationship_with_merge
            pass
        elif choice == "12":
            # Placeholder for create_relationship_with_create
            pass
        elif choice == "13":
            # Placeholder for add_properties_to_relationship
            pass
        elif choice == "14":
            # Placeholder for add_properties_to_multiple_relationships
            pass
        elif choice == "15":
            # Placeholder for update_properties_for_relationship
            pass
        elif choice == "16":
            # Placeholder for update_properties_for_multiple_relationships
            pass
        elif choice == "17":
            # Placeholder for delete_properties_from_relationship
            pass
        elif choice == "18":
            # Placeholder for delete_properties_from_multiple_relationships
            pass
        elif choice == "19":
            # Placeholder for show_entities
            pass
        elif choice == "20":
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