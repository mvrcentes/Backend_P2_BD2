from faker import Faker
import random
from nodes_relationships import *

fake = Faker()

generos_videojuegos = [
    "RPG", "FPS", "MOBA", "Aventura", "Estrategia", "Action", "MMORPG", "Multiplayer",
    "Plataforma", "Simulación", "Deportes", "Carreras", "Puzle", "Sandbox", "Horror",
    "Sigilo", "Hack and Slash", "RTS", "CCG", "TBS", "Fighting", "Music/Rhythm", "TPS",
    "Survival", "Open World", "Educational", "Puzzle Platformer", "Building/Management",
    "Survival Horror", "Graphic Adventure", "Tactical RPG", "RTS", "TBS-Hex", "Action RPG",
    "Exploration", "Extreme Sports", "Tactical Shooter", "Platform Fighting", "Kart Racing",
    "Action MMORPG", "Point-and-Click Adventure", "Life Simulation", "TPS with RPG Elements",
    "RTT", "Weapon-Based Fighting", "City Building Strategy", "Tower Defense Strategy",
    "Online Multiplayer Shooter", "Survival Arena Shooter", "FPS with RPG Elements"
]

plataformas_videojuegos = [
    "PC", "PlayStation 5", "PlayStation 4", "PlayStation 3", "PlayStation 2", "PlayStation",
    "Xbox Series X", "Xbox One", "Xbox 360", "Xbox", "Nintendo Switch", "Wii U", "Wii",
    "Nintendo 3DS", "Nintendo DS", "GameCube", "Game Boy Advance", "Game Boy Color", "Game Boy",
    "Nintendo 64", "Super Nintendo Entertainment System (SNES)", "Nintendo Entertainment System (NES)",
    "Sega Dreamcast", "Sega Saturn", "Sega Genesis", "Sega Master System", "Atari 2600",
    "Arcade", "Mobile"
]

clasificaciones_por_edades = [
    "EC (Early Childhood)","E (Everyone)","E10+ (Everyone 10 and Older)",
    "T (Teen)","M (Mature)","AO (Adults Only)","RP (Rating Pending)"
]

niveles_complejidad = [
    "Baja",
    "Media",
    "Alta"
]


# Función para generar usuarios ficticios
def generate_fake_users(num_users):
    for _ in range(num_users):
        user_properties = {
            "nombre": fake.name(),
            "edad": random.randint(18, 50),
            "email": fake.email(),
            "activo": random.choice([True, False]),
            "generos_favoritos": random.sample(generos_videojuegos, random.randint(1, 4))
        }
        create_user(user_properties)

# Función para generar videojuegos ficticios
def generate_fake_games(num_games):
    for _ in range(num_games):
        game_properties = {
            "titulo": fake.sentence(nb_words=3),
            "precio": round(random.uniform(1.0, 100.0), 2),
            "lanzamiento": fake.date_this_decade(),
            "clasificacion": random.choice(clasificaciones_por_edades),
            "multiplayer": random.choice([True, False]),
        }
        create_video_game(game_properties)

# Función para generar géneros ficticios
def generate_fake_genres():
    for genre_name in generos_videojuegos:
        # Verificar si el género ya existe
        genre_node = graph.nodes.match("GENERO", nombre=genre_name).first()
        
        if not genre_node:
            genre_properties = {
                "nombre": genre_name,
                "descripcion": fake.sentence(nb_words=6),
                "inmersion": random.choice(niveles_complejidad),
                "complejidad": random.choice(niveles_complejidad),
                "interactividad": random.choice(niveles_complejidad),
            }
            create_genre(genre_properties)
        else:
            print(f"El género {genre_name} ya existe.")

def generate_fake_platforms():
    for platform_name in plataformas_videojuegos:
        # Verificar si la plataforma ya existe
        platform_node = graph.nodes.match("PLATAFORMA", nombre=platform_name).first()
        
        if not platform_node:
            platform_properties = {
                "nombre": platform_name,
                "fabricante": fake.company(),
                "fecha_creacion": fake.date_this_century(),
                "generacion": random.randint(1, 5),
                "precio": round(random.uniform(100.0, 1200.0), 2),
            }
            create_platform(platform_properties)
        else:
            print(f"La plataforma {platform_name} ya existe.")


# Función para generar reseñas ficticias
def generate_fake_reviews(num_reviews):
    for _ in range(num_reviews):
        review_properties = {
            "titulo": fake.sentence(nb_words=6),
            "contenido": fake.paragraph(nb_sentences=3),
            "calificación": random.randint(1, 10),
            "fecha": fake.date_between(start_date="-2y", end_date="today"),
            "util": random.choice([True, False])
        }
        create_review(review_properties)

# Función para generar distribuidoras ficticias
def generate_fake_publishers(num_publishers):
    for _ in range(num_publishers):
        publisher_properties = {
            "nombre": fake.company(),
            "fundación": fake.date_this_century(),
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
            "edicion": random.choice([1, 2, 3, 4, 5]),  # List of integers for editions
            "fecha_publicacion": fake.date_between(start_date="-2y", end_date="today"),    
        }
        create_guide(guide_properties)

def generate_fake_relationships(num_relationships):
    users = [user['nombre'] for user in graph.run("MATCH (u:GAMER) RETURN u.nombre AS nombre").data()]
    games = [game['titulo'] for game in graph.run("MATCH (g:JUEGO) RETURN g.titulo AS titulo").data()]
    genres = [genre['nombre'] for genre in graph.run("MATCH (g:GENERO) RETURN g.nombre AS nombre").data()]
    platforms = [platform['nombre'] for platform in graph.run("MATCH (p:PLATAFORMA) RETURN p.nombre AS nombre").data()]
    reviews = [review['titulo'] for review in graph.run("MATCH (r:REVIEW) RETURN r.titulo AS titulo").data()]
    guides = [guide['titulo'] for guide in graph.run("MATCH (g:GUIA) RETURN g.titulo AS titulo").data()]
    publishers = [publisher["nombre"] for publisher in graph.run("MATCH (p:DISTRIBUIDORA) RETURN p.nombre AS nombre").data()]
    
    for _ in range(num_relationships):
        user_id = random.choice(users)
        game_id = random.choice(games)
        genre = random.choice(genres)
        platform = random.choice(platforms)
        if reviews:
            review = random.choice(reviews)
        if guides:
            guide = random.choice(guides)
        publisher_id = random.choice(publishers)
        
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

        # Generar relaciones de publicación
        cant_distribuida = random.randint(10000,100000)
        territories = [fake.country() for _ in range(4)]
        date_publish = fake.date_between(start_date="-2y", end_date="today")

        publisher_publishes_game(publisher_id, game_id, cant_distribuida, territories, date_publish)





def review_rates(review_id, entity_type, entity_id, date, stars, verified):
    review_node = graph.nodes.match("REVIEW", titulo=review_id).first()

    # Determinar la etiqueta del nodo según el tipo de entidad
    if entity_type == "JUEGO":
        entity_node = graph.nodes.match("JUEGO", titulo=entity_id).first()
    elif entity_type == "GENERO":
        entity_node = graph.nodes.match("GENERO", nombre=entity_id).first()
    elif entity_type == "DISTRIBUIDORA":
        entity_node = graph.nodes.match("DISTRIBUIDORA", nombre=entity_id).first()
    elif entity_type == "PLATAFORMA":
        entity_node = graph.nodes.match("PLATAFORMA", nombre=entity_id).first()
    else:
        print(f"Tipo de entidad no válido: {entity_type}")
    return None

# Generar datos ficticios

#generate_fake_genres()
#generate_fake_platforms()
#generate_fake_users(500)
#generate_fake_games(1000)
#generate_fake_reviews(80)
#generate_fake_publishers(30)
#generate_fake_guides(75)
generate_fake_relationships(300)
