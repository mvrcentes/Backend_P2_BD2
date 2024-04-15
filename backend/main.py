# main.py (actualización)

from crud import *
from nodes_relationships import *
from admin import *

def main():
    print("Bienvenido al sistema de recomendaciones de videojuegos!")
    
    # Iniciar sesión
    user_email = input("Por favor, introduzca su correo electrónico para iniciar sesión: ")

     # Verificar si el correo es el del administrador
    if user_email == "admin@ejemplo.com":
        print("Acceso de administrador concedido.")
        admin_menu()
        return

    user_node = graph.nodes.match("USUARIO", email=user_email).first()
    
    if user_node:
        print(f"Bienvenido de nuevo, {user_node['nombre']}!")
    else:
        print("Usuario no encontrado.")
        create_new_user = input("¿Desea crear un nuevo usuario? (yes/no): ")
        if create_new_user.lower() == "yes":
            if create_user():
                print("Usuario creado exitosamente.")
            else:
                print("Ese correo ya está en uso. Usuario Actualizado")
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
            recommended_games = recommend_games_for_user(user_node['nombre'])
            games_list = list(recommended_games)

            if games_list:
                headers = ["Título", "Plataformas", "Fecha de Lanzamiento", "Género", "Rating"]
                header_format = "{:<20} | {:<50} | {:<20} | {:<10} | {:<10}"

                print(header_format.format(*headers))
                print("-" * 20 + "|" + "-" * 50 + "|" + "-" * 20 + "|"  + "-" * 10 + "|" + "-" * 10)

                for record in games_list:
                    titulo = record['Titulo'][:20].ljust(20)
                    plataformas = str(record['Plataformas'])[:50].ljust(50)
                    fecha = str(record['Fecha_de_Lanzamiento'])[:20].ljust(20)
                    genero = str(record['Genero'])[:10].ljust(10)
                    rating = str(record['Rating'])[:10].ljust(10)

                    print(f"{titulo} | {plataformas} | {fecha} | {genero} | {rating}")
            else:
                print("No se encontraron juegos recomendados.")

        elif choice == "2":
            genre = input("Introduzca el género que desea buscar: ")
            games_by_genre = find_games_by_genre(genre)
            games_list = list(games_by_genre)

            if games_list:
                print("Recomendaciones basadas en el género seleccionado:\n")
                headers = ["Título", "Plataformas", "Fecha_de_Lanzamiento"]
                header_format = "{:<30} | {:<50} | {:<20}"

                print(header_format.format(*headers))
                print("-" * 30 + "|" + "-" * 50 + "|" + "-" * 20)

                for record in games_list:
                    titulo = record['Titulo'][:30].ljust(30)
                    plataformas = str(record['Plataformas'])[:50].ljust(50)
                    fecha = str(record['Fecha_de_Lanzamiento'])[:20].ljust(20)

                    print(f"{titulo} | {plataformas} | {fecha}")
            else:
                print(f"No se encontraron juegos para el género {genre}.")
        elif choice == "3":
            # Funcionalidad para jugar un juego
            pass
        elif choice == "4":
            review_properties = {
                "titulo": input("Introduzca el título de la reseña: "),
                "contenido": input("Escriba su reseña: "),
                "calificacion": int(input("Califique el juego (1-5): ")),
                "fecha": input("Introduzca la fecha de la reseña (YYYY-MM-DD): "),
                "util": input("¿Recomienda este juego? (True/False): ").lower() == "true"
            }
            review_node = create_review(review_properties)
            
            if review_node:
                user_reviewed_game(user_node['nombre'], review_properties["titulo"], review_properties["fecha"], review_properties["calificacion"], review_properties["util"])
                print("Reseña creada exitosamente y relación establecida.")
            else:
                print("Error al crear la reseña.")
            pass
        elif choice == "5":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()