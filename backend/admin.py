

def admin_menu():

    while True:
        print("\nMenú de Administrador:")
        print("1. Crear un nuevo juego")
        print("2. Crear un nuevo usuario")
        print("3. Salir")
        
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