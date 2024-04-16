# main.py (actualización)

from user import *
from nodes_relationships import *
from admin import *

def main():
    print("Bienvenido al sistema de recomendaciones de videojuegos!\n")
    logged_in = False
    more_options = False
    
    # Iniciar sesión
    user_email = input("Por favor, introduzca su correo electrónico para iniciar sesión o exit para salir: ")

    if user_email.lower() == "exit":
        print("Saliendo del sistema.")
        return

     # Verificar si el correo es el del administrador
    if user_email == "admin@ejemplo.com":
        print("Acceso de administrador concedido.")
        admin_menu()
        return

    user_node = graph.nodes.match("USUARIO", email=user_email).first()
    
    if user_node:
        logged_in = True
        print(f"Bienvenido de nuevo, {user_node['nombre']}!\n")
    else:
        print("Usuario no encontrado.")
        create_new_user = input("¿Desea crear un nuevo usuario? (yes/no): ")
        if create_new_user.lower() == "yes":
            if create_user_Main():
                print("Usuario creado exitosamente.")
            else:
                print("Ese correo ya está en uso. Usuario Actualizado")
            main()
        else:
            print("\nSaliendo del sistema.")
            return
    
    # Menú principal
    while logged_in:
        print("\nMenú principal:")
        print("1. Recomendar juegos basados en los generos que te gustan")
        print("2. Recomendar juegos basados en tus juegos jugados\n")
        print("3. Buscar juegos por género")
        print("4. Buscar juegos\n")
        print("5. Agregar juego a mis jugados")
        print("6. Ver mis juegos\n")
        print("7. Escribir una reseña")
        print("8. Ver reseñas\n")
        print("9. Más opciones\n")
        print("10. Salir\n")
        
        choice = input("Por favor, seleccione una opción: ")
        
        if choice == "1":
            print("Recomendaciones basadas en sus preferenciasn de géneros:")
            recommended_games = recommend_games_for_user_genres(user_node['nombre'])
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
            print("Recomendaciones basadas en sus juegos jugados:")
            recommended_games = recommend_games_for_user(user_node['nombre'])
            games_list = list(recommended_games)

            if games_list:
                headers = ["Título", "Plataformas", "Fecha de Lanzamiento", "Score"]
                header_format = "{:<20} | {:<50} | {:<20} | {:<10}"

                print(header_format.format(*headers))
                print("-" * 20 + "|" + "-" * 50 + "|" + "-" * 20 + "|"  + "-" * 10)

                for record in games_list:
                    titulo = record['title'][:20].ljust(20)
                    plataformas = str(record['platform'])[:50].ljust(50)
                    fecha = str(record['release_date'])[:20].ljust(20)
                    score = str(record['score'])[:10].ljust(10)

                    print(f"{titulo} | {plataformas} | {fecha} | {score}")
            else:
                print("No se encontraron juegos recomendados.")
        elif choice == "3":
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
        elif choice == "4":
            # Funcionalidad para buscar un juego
            titulo = input("Introduzca el título del juego que desea buscar: ")
            games_by_title = find_games_by_title(titulo)
            games_list = list(games_by_title)

            if games_list:
                print("Resultados de la búsqueda:\n")
                headers = ["Título", "Plataformas", "Fecha de Lanzamiento"]
                header_format = "{:<30} | {:<50} | {:<20}"

                print(header_format.format(*headers))
                print("-" * 30 + "|" + "-" * 50 + "|" + "-" * 20)

                for record in games_list:
                    titulo = record['Titulo'][:30].ljust(30)
                    plataformas = str(record['Plataformas'])[:50].ljust(50)
                    fecha = str(record['Fecha_de_Lanzamiento'])[:20].ljust(20)

                    print(f"{titulo} | {plataformas} | {fecha}")
            else:
                print(f"No se encontraron juegos con el título {titulo}.")
        elif choice == "5":
            # Funcionalidad jugar juego
            titulo = input("Introduzca el título del juego que desea agregar a sus jugados: ")
            game_node = graph.nodes.match("VIDEOJUEGO", titulo=titulo).first()

            if game_node:
                horas_jugadas = int(input("Introduzca las horas jugadas: "))
                desde = input("Introduzca la fecha de inicio de juego (YYYY-MM-DD): ")
                favorito = input("¿Es este juego uno de sus favoritos? (True/False): ").lower() == "true"
                user_plays_game(user_node['nombre'], game_node['titulo'], desde, horas_jugadas, favorito)
                print("Juego añadido a su lista de jugados.")
            else:
                print(f"No se encontró el juego con el título {titulo}.")

        elif choice == "6":
            user_games = get_user_games(user_node['email'])
            games_list = list(user_games)

            if games_list:
                print("Juegos jugados por el usuario:\n")
                headers = ["Título", "Horas Jugadas", "Jugado Desde"]
                header_format = "{:<30} | {:<30} | {:<20}"

                print(header_format.format(*headers))
                print("-" * 30 + "|" + "-" * 30 + "|" + "-" * 20)

                for record in games_list:
                    titulo = record['Titulo'][:30].ljust(30)
                    horas = str(record['Horas'])[:30].ljust(30)
                    fecha = str(record['Jugado_Desde'])[:20].ljust(20)

                    print(f"{titulo} | {horas} | {fecha}")
            else:
                print("No se encontraron juegos jugados.")

        elif choice == "7":
            entity_type = input("¿Qué desea calificar? (JUEGO/GENERO/DISTRIBUIDORA/PLATAFORMA): ").upper()
            entity_id = input(f"Introduzca el nombre del {entity_type}: ")
            
            if check_entity_exists(entity_type, entity_id):
                review_properties = {
                    "titulo": input("Introduzca el título de la reseña: "),
                    "contenido": input("Escriba su reseña: "),
                    "calificacion": int(input(f"Califique {entity_type} (1-5): ")),
                    "fecha": input("Introduzca la fecha de la reseña (YYYY-MM-DD): "),
                    "util": input(f"¿Recomienda {entity_type}? (True/False): ").lower() == "true"
                }
                
                review_node = create_review(review_properties)
                
                if review_node:
                    user_reviewed_game(user_node['nombre'], review_node['titulo'], review_properties["fecha"], review_properties["calificacion"], review_properties["util"])
                    review_rates(review_node['titulo'], entity_type, entity_id, review_properties["fecha"], review_properties["calificacion"], review_properties["util"])
                    print("Reseña creada exitosamente y relación establecida.")
                else:
                    print("Error al crear la reseña.")
            else:
                print(f"No se encontró {entity_type} con el nombre {entity_id}.")

        elif choice == "8":
            get_user_reviews(user_node['nombre'])
        elif choice == "9":
            more_options = True
            while more_options:
                print("\nMás opciones:")
                print("1. Juegos más populares por género")
                print("2. Mejores juegos")
                print("3. Gamers más activos")
                print("4. Juegos con más plataformas")
                print("5. Regresar al menú principal\n")
                
                choice = input("Por favor, seleccione una opción: ")
                
                if choice == "1":
                    friends_games = most_popular_games_by_genre()
                    games_list = list(friends_games)

                    if games_list:
                        print("Juegos más populares por género:\n")
                        headers = ["Género", "Título", "Rating"]
                        header_format = "{:<33} | {:<33} | {:<33}"

                        print(header_format.format(*headers))
                        print("-" * 33 + "|" + "-" * 33 + "|" + "-" * 33)

                        for record in games_list:
                            titulo = record['Titulo'][:33].ljust(33)
                            genero = str(record['Genero'])[:33].ljust(33)
                            rating = str(record['Numero_de_Reseñas'])[:33].ljust(33)

                            print(f"{genero} | {titulo} | {rating}")
                    else:
                        print("No se encontraron juegos.")
                elif choice == "2":
                    top_rated = top_rated_games_overall()
                    games_list = list(top_rated)

                    if games_list:
                        print("Mejores juegos:\n")
                        headers = ["Título", "Plataformas"]
                        header_format = "{:<30} | {:<50}"

                        print(header_format.format(*headers))
                        print("-" * 30 + "|" + "-" * 50)

                        for record in games_list:
                            titulo = record['Titulo'][:30].ljust(30)
                            rating = str(record['Plataformas'])[:50].ljust(50)

                            print(f"{titulo} | {rating}")
                    else:
                        print("No se encontraron juegos recomendados.")
                elif choice == "3":
                    active_users = most_active_gamers()
                    users_list = list(active_users)

                    if users_list:
                        print("Gamers más activos:\n")
                        headers = ["Nombre", "Horas Totales"]
                        header_format = "{:<30} | {:<30}"

                        print(header_format.format(*headers))
                        print("-" * 30 + "|" + "-" * 30)

                        for record in users_list:
                            nombre = record['Gamer'][:30].ljust(30)
                            horas = str(record['Horas_Totales'])[:30].ljust(30)

                            print(f"{nombre} | {horas}")
                elif choice == "4":
                    games_platforms = games_with_most_diverse_platforms()
                    games_list = list(games_platforms)

                    if games_list:
                        print("Juegos con más plataformas:\n")
                        headers = ["Título", "Plataformas"]
                        header_format = "{:<30} | {:<50}"

                        print(header_format.format(*headers))
                        print("-" * 30 + "|" + "-" * 50)

                        for record in games_list:
                            titulo = record['Titulo'][:30].ljust(30)
                            plataformas = str(record['Numero_de_Plataformas'])[:50].ljust(50)

                            print(f"{titulo} | {plataformas}")
                    else:
                        print("No se encontraron juegos.")
                elif choice == "5":
                    more_options = False
                else:
                    print("Opción no válida. Por favor, intente de nuevo.")
        elif choice == "10":
            print("Saliendo del sistema.")
            logged_in = False
            main()
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()