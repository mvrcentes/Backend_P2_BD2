from crud import *

def add_properties_for_relation(matcher, start_node_label, start_node_property_name, start_node_property_value, relationship_type, end_node_label, end_node_property_name, end_node_property_value, **properties):
    start_node = matcher.match(start_node_label).where(f"_.{start_node_property_name} = '{start_node_property_value}'").first()
    end_node = matcher.match(end_node_label).where(f"_.{end_node_property_name} = '{end_node_property_value}'").first()
    relation = Relationship(start_node, relationship_type, end_node, **properties)
    graph.push(relation)


# PUBLISHER
def create_publisher():
    publisher_properties = {
      "nombre": str,
      "fundacion": str,  
      "pais": str,
      "sitio_web": str
    }
    publisher_data = request_data(publisher_properties)
    merge_node(["DISTRIBUIDORA"], "nombre", publisher_data["nombre"], **publisher_data)

def update_publisher():
    publisher_properties = {
      "nombre": str,
      "fundacion": str,  
      "pais": str,
      "sitio_web": str
    }

    publisher_name = input("Introduzca el nombre de la distribuidora que desea actualizar: ")
    publisher_node = graph.nodes.match("DISTRIBUIDORA").where(f"_.nombre = '{publisher_name}'").first()
    if publisher_node:
        publisher_data = request_data(publisher_properties)
        merge_node(["DISTRIBUIDORA"], "nombre", publisher_name, **publisher_data)
    else:
        print("Distribuidora no encontrada.")

def delete_publisher():
    publisher_name = input("Introduzca el nombre de la distribuidora que desea eliminar: ")
    publisher_node = graph.nodes.match("DISTRIBUIDORA").where(f"_.nombre = '{publisher_name}'").first()
    if publisher_node:
        delete_node(publisher_node)
    else:
        print("Distribuidora no encontrada.")

def add_properties_to_publisher():
    # pregunta por el nombre de la distribuidora
    publisher_name = input("Introduzca el nombre de la distribuidora a la que desea agregar propiedades: ")
    #comprueba si la distribuidora existe
    publisher_node = graph.nodes.match("DISTRIBUIDORA").where(f"_.nombre = '{publisher_name}'").first()
    # si la distribuidora existe pregunta por las propiedades a agregar
    if publisher_node:
        input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
        properties = dict(item.split(":") for item in input_properties.split(","))
        add_properties_for_node(NodeMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_name, **properties)

def add_properties_to_multiple_publishers():
    # pregunta por los nombres de las distribuidoras
    publisher_names = input("Introduzca los nombres de las distribuidoras a las que desea agregar propiedades separadas por comas: ")
    publisher_names_list = [f"'{name.strip()}'" for name in publisher_names.split(",")]
    # verificar si las distribuidoras existen
    query = (
        "MATCH (d:DISTRIBUIDORA) "
        f"WHERE d.nombre IN [{','.join(publisher_names_list)}] "
        "RETURN d"
    )
    publisher_nodes = graph.run(query).data()
    # si las distribuidoras existen pregunta por las propiedades a agregar
    if publisher_nodes:
        input_properties = input("Introduzca las propiedades a agregar en formato clave:valor separadas por comas: ")
        properties = dict(item.split(":") for item in input_properties.split(","))
        
        for publisher_node in publisher_nodes:
            add_properties_for_node(NodeMatcher(graph), "DISTRIBUIDORA", "nombre", publisher_node["d"]["nombre"], **properties)

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

# opcion 7 
def add_properties_to_publisher_game_relationships():
    # Solicitar el nombre de la distribuidora
    distributor_name = input("Introduzca el nombre de la distribuidora: ")

    # Solicitar los títulos de los juegos
    games_input = input("Introduzca los títulos de los juegos a los que desea agregar propiedades, separados por comas: ")
    games = games_input.split(",")

    # Solicitar las propiedades a agregar
    properties_input = input("Introduzca las propiedades a agregar en formato clave:valor, separadas por comas: ")
    properties = dict(item.split(":") for item in properties_input.split(","))

    # Verificar si la distribuidora existe
    query = (
        "MATCH (d:DISTRIBUIDORA) "
        f"WHERE d.nombre = '{distributor_name}' "
        "RETURN d"
    )
    distributor_node = graph.run(query).data()

    # Si la distribuidora existe
    if distributor_node:
        # Para cada juego, agregar las propiedades a la relación con la distribuidora
        for game_title in games:
            query = (
                f"MATCH (:DISTRIBUIDORA {{nombre: '{distributor_name}'}})-[r:DISTRIBUYE]->(:JUEGO {{titulo: '{game_title}'}}) "
                "SET r += $properties"
            )
            graph.run(query, properties=properties)

# opcion 9
def delete_properties_from_publishers():
    # Solicitar los nombres de las distribuidoras
    publisher_names_input = input("Introduzca los nombres de las distribuidoras a las que desea eliminar propiedades, separados por comas: ")
    publisher_names = [name.strip() for name in publisher_names_input.split(",")]

    # Solicitar las propiedades a eliminar
    properties_input = input("Introduzca las propiedades a eliminar en formato clave, separadas por comas: ")
    properties = properties_input.split(",")

    # Para cada distribuidora, eliminar las propiedades especificadas
    for publisher_name in publisher_names:
        query = (
            f"MATCH (d:DISTRIBUIDORA {{nombre: '{publisher_name}'}}) "
            f"REMOVE {', '.join([f'd.{prop}' for prop in properties])}"
        )
        graph.run(query)

def menu_distribuidora():
    print("Menú de Distribuidora:")
    print("1. Crear Distribuidora")
    print("2. Actualizar Distribuidora")
    print("3. Eliminar Distribuidora")
    print("4. Agregar 1 o mas propiedades a una distribuidora")
    print("5. Agregar 1 o mas propiedades a multiples distribuidoras")
    print("6. Agregar 1 o mas propiedades a una relacion de la distribuidora")
    print("7. Agregar 1 o mas propiedades a multiples relaciones de la distribuidora")
    print("8. Eliminar 1 o mas propiedades de una distribuidora")
    print("9. Eliminar 1 o mas propiedades de multiples distribuidoras")
    print("10. Eliminar 1 o mas propiedades de una relacion de la distribuidora")
    print("11. Eliminar 1 o mas propiedades de multiples relaciones de la distribuidora")
    print("12. Ver Distribuidoras")
    print("13. Regresar")
    
    choice = input("Por favor, seleccione una opción: ")
    
    if choice == "1":
        print("\n\n----Creando Distribuidora----")
    
        create_publisher()
        
    elif choice == "2":
        update_publisher()
    elif choice == "3":
        delete_publisher()
    elif choice == "4":
        add_properties_to_publisher()
    elif choice == "5":
        add_properties_to_multiple_publishers()
    elif choice == "6":
        add_properties_to_publisher_relationship()
    elif choice == "7":
        add_properties_to_publisher_game_relationships()
    elif choice == "8":
        delete_properties_from_publisher()
    elif choice == "9":
        delete_properties_from_publishers()
    elif choice == "10":
        delete_properties_from_publisher_relationship()
    elif choice == "12":
        view_publishers()
    elif choice == "13":
        return
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")



def admin_menu():

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
        
        if choice == "1":
            menu_distribuidora()
        elif choice == "2":
            menu_juegos()
        elif choice == "3":
            menu_guia_juegos()
        elif choice == "4":
            menu_usuarios()
        elif choice == "5":
            menu_plataformas()
        elif choice == "6":
            menu_resenas()
        elif choice == "7":
            menu_generos()
        elif choice == "8":
            print("Saliendo del sistema.")
            return
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")