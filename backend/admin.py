
def menu_distribuidora():
    print("Menú de Distribuidora:")
    print("1. Crear Distribuidora")
    print("2. Actualizar Distribuidora")
    print("3. Eliminar Distribuidora")
    print("4. Agregar 1 o mas propiedade")
    print("4. Ver Distribuidoras")
    print("5. Salir")
    
    choice = input("Por favor, seleccione una opción: ")
    
    if choice == "1":
        create_distributor()
    elif choice == "2":
        update_distributor()
    elif choice == "3":
        delete_distributor()
    elif choice == "4":
        view_distributors()
    elif choice == "5":
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
            create_new_game()
        elif choice == "2":
            create_user()
        elif choice == "3":
            print("Saliendo del sistema.")
            return
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")