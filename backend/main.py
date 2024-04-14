# main.py (actualización)

from crud import *

def main():
    print("Bienvenido al sistema de recomendaciones de videojuegos!")
    
    # Iniciar sesión
    user_email = input("Por favor, introduzca su correo electrónico para iniciar sesión: ")
    user_node = graph.nodes.match("USUARIO", email=user_email).first()
    
    if user_node:
        print(f"Bienvenido de nuevo, {user_node['nombre']}!")
    else:
        print("Usuario no encontrado.")
        create_new_user = input("¿Desea crear un nuevo usuario? (yes/no): ")
        if create_new_user.lower() == "yes":
            create_user()
            print("Usuario creado exitosamente. Por favor, inicie sesión nuevamente.")
            main()
        else:
            print("Saliendo del sistema.")
            return
    
    # Menú principal
    while True:
        print("\nMenú principal:")
        print("1. Recomendar juegos")
        print("2. Buscar juegos por género")
        print("3. Jugar un juego")
        print("4. Escribir una reseña")
        print("5. Salir")
        
        choice = input("Por favor, seleccione una opción: ")
        
        if choice == "1":
            print("Recomendaciones basadas en sus preferencias:")
            print(recommend_games_for_user(user_node['id']))
        elif choice == "2":
            genre = input("Introduzca el género que desea buscar: ")
            print("Recomendaciones basadas en el género seleccionado:")
            print(find_games_by_genre(genre))
        elif choice == "3":
            # Funcionalidad para jugar un juego
            pass
        elif choice == "4":
            # Funcionalidad para escribir una reseña
            pass
        elif choice == "5":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()