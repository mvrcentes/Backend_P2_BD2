from faker import Faker
import random
from nodes_relationships import *

fake = Faker()

# Función para generar usuarios ficticios
def generate_fake_users(num_users):
    for _ in range(num_users):
        user_properties = {
            "nombre": fake.name(),
            "edad": random.randint(18, 50),
            "email": fake.email(),
            "activo": random.choice([True, False]),
            "generos_favoritos": random.sample(["RPG", "FPS", "MOBA", "Aventura", "Estrategia", "Action", "MMORPG", "Multiplayer"], random.randint(1, 3))
        }
        create_user(user_properties)

# Función para generar videojuegos ficticios
def generate_fake_games(num_games):
    for _ in range(num_games):
        game_properties = {
            "titulo": fake.sentence(nb_words=3),
            "precio": round(random.uniform(10.0, 60.0), 2),
            "lanzamiento": fake.date_this_decade(),
            "plataformas": random.sample(['PC', 'PS4', 'Xbox One', 'Switch', 'PS5', 'Xbox Series X'], random.randint(1, 4)),
            "multiplayer": random.choice([True, False]),
        }
        create_video_game(game_properties)

# Función para generar géneros ficticios
def generate_fake_genres():
    genres_list = ["RPG", "FPS", "MOBA", "Aventura", "Estrategia", "Action", "MMORPG", "Multiplayer"]
    
    for genre_name in genres_list:
        # Verificar si el género ya existe
        genre_node = graph.nodes.match("GENERO", nombre=genre_name).first()
        
        if not genre_node:
            genre_properties = {
                "nombre": genre_name,
                "popularidad": random.randint(1, 100),
                "descripcion": fake.sentence(nb_words=6),
                "promedio_calificacion": round(random.uniform(1.0, 10.0), 1),
                "juegos": random.randint(1, 100000)
            }
            create_genre(genre_properties)
        else:
            print(f"El género {genre_name} ya existe.")

# Función para generar plataformas ficticias
def generate_fake_platforms(num_platforms):
    for _ in range(num_platforms):
        platform_properties = {
            "nombre": random.choice(['PC', 'PS4', 'Xbox One', 'Switch', 'PS5', 'Xbox Series X']),
            "fabricante": fake.company(),
            "fecha_lanzamiento": fake.date_this_decade(),
            "disponible": random.choice([True, False]),
            "exclusivos": random.sample(["RPG", "FPS", "MOBA", "Aventura", "Estrategia", "Action", "MMORPG", "Multiplayer"], random.randint(1, 3))
        }
        create_platform(platform_properties)

# Función para generar reseñas ficticias
def generate_fake_reviews(num_reviews):
    for _ in range(num_reviews):
        review_properties = {
            "titulo": fake.sentence(nb_words=6),
            "contenido": fake.paragraph(nb_sentences=3),
            "calificacion": random.randint(1, 10),
            "fecha": fake.date_between(start_date="-2y", end_date="today"),
            "util": random.choice([True, False])
        }
        create_review(review_properties)

# Función para generar distribuidoras ficticias
def generate_fake_publishers(num_publishers):
    for _ in range(num_publishers):
        publisher_properties = {
            "nombre": fake.company(),
            "fundacion": fake.date_this_century(),
            "pais": fake.country(),
            "sitio_web": fake.url(),
            "sucursales": [fake.country() for _ in range(5)],
        }
        create_publisher(publisher_properties)

def generate_fake_guides(num_guides):
    for _ in range(num_guides):
        guide_properties = {
            "titulo": fake.sentence(nb_words=6),
            "contenido": fake.paragraph(nb_sentences=3),
            "autor": fake.name(),
            "fecha_publicacion": fake.date_between(start_date="-2y", end_date="today"),
            "etiquetas": random.sample(["RPG", "FPS", "MOBA", "Aventura", "Estrategia", "Action", "MMORPG", "Multiplayer"], random.randint(1, 3))
        }
        create_guide(guide_properties)

# Función para generar relaciones ficticias
def generate_fake_relationships(num_relationships):
    users = [user['nombre'] for user in graph.run("MATCH (u:GAMER) RETURN u.nombre AS nombre").data()]
    games = [game['titulo'] for game in graph.run("MATCH (g:JUEGO) RETURN g.titulo AS titulo").data()]
    genres = [genre['nombre'] for genre in graph.run("MATCH (g:GENERO) RETURN g.nombre AS nombre").data()]
    platforms = [platform['nombre'] for platform in graph.run("MATCH (p:PLATAFORMA) RETURN p.nombre AS nombre").data()]
    reviews = [review['titulo'] for review in graph.run("MATCH (r:REVIEW) RETURN r.titulo AS titulo").data()]
    guides = [guide['titulo'] for guide in graph.run("MATCH (g:GUIA) RETURN g.titulo AS titulo").data()]
    
    for _ in range(num_relationships):
        user_id = random.choice(users)
        game_id = random.choice(games)
        genre = random.choice(genres)
        platform = random.choice(platforms)
        if reviews:
            review = random.choice(reviews)
        if guides:
            guide = random.choice(guides)
        
        since = fake.date_between(start_date="-2y", end_date="today")
        hours_played = random.randint(1, 100)
        favorite = random.choice([True, False])
        
        user_plays_game(user_id, game_id, since, hours_played, favorite)
        
        date = fake.date_between(start_date="-2y", end_date="today")
        rating = random.randint(1, 10)
        recommends = random.choice([True, False])
        
        user_reviewed_game(user_id, review, date, rating, recommends)
        
        stars = random.randint(1, 5)
        verified = random.choice([True, False])
        review_type = random.choice(["JUEGO", "GENERO", "PLATAFORMA", "DISTRIBUIDORA"])
        
        review_rates(review, review_type, game_id, date, stars, verified)
        
        digital_format = random.choice([True, False])
        special_edition = random.choice([True, False])
        
        game_available_on_platform(game_id, platform, date, digital_format, special_edition)
        
        exclusive = random.choice([True, False])
        average_rating = round(random.uniform(1.0, 10.0), 1)
        
        game_belongs_to_genre(game_id, genre, date, exclusive, average_rating)

        guide_stars = random.randint(1, 5)
        guide_belongs_to_game(guide, game_id, guide_stars)

        # Eliminar la revisión seleccionada de la lista de revisiones
        if review in reviews:
            reviews.remove(review)
        if guide in guides:
            guides.remove(guide)

def generate_fake_publish_relationships(num_relationships):
    publishers = [publisher["nombre"] for publisher in graph.run("MATCH (p:DISTRIBUIDORA) RETURN p.nombre AS nombre").data()]
    games = [game['titulo'] for game in graph.run("MATCH (g:JUEGO) RETURN g.titulo AS titulo").data()]

    for _ in range(num_relationships):
        publisher_id = random.choice(publishers)
        game_id = random.choice(games)

        cant_distribuida = random.randint(10000,100000)
        territories = [fake.country() for _ in range(4)]
        date = fake.date_between(start_date="-2y", end_date="today")

        publisher_publishes_game(publisher_id, game_id, cant_distribuida, territories, date)


# Generar datos ficticios
# generate_fake_users(500)
# generate_fake_games(700)
# # generate_fake_genres()
# generate_fake_reviews(100)
# generate_fake_platforms(5)
# generate_fake_publishers(10)
# generate_fake_guides(50)
# generate_fake_relationships(500)

generate_fake_publish_relationships(600)