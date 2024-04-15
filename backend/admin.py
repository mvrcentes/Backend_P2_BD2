from crud import *



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
        add_properties_to_multiple_publisher_relationships()
    elif choice == "8":
        delete_properties_from_publisher()
    elif choice == "9":
        delete_properties_from_multiple_publishers()
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
            menu_publisher()
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