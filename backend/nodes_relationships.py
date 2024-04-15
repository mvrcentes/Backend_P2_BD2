from crud import *

# CREATE NODES
def create_user(user_properties):
    labels = ["USUARIO", "GAMER"]
    return create_node(labels, **user_properties)

def create_video_game(game_properties):
    labels = ["VIDEOJUEGO", "JUEGO"]
    return create_node(labels, **game_properties)

def create_genre(genre_properties):
    labels = ["GENERO"]
    return create_node(labels, **genre_properties)

def create_review(review_properties):
    labels = ["REVIEW", "CRITICA"]
    return create_node(labels, **review_properties)

def create_platform(platform_properties):
    labels = ["PLATAFORMA"]
    return create_node(labels, **platform_properties)

def create_publisher(publisher_properties):
    labels = ["DISTRIBUIDORA"]
    return create_node(labels, **publisher_properties)

def create_guide(guide_properties):
    labels = ["GUIA"]
    return create_node(labels, **guide_properties)

def user_plays_game(user_id, game_id, since, hours_played, favorite):
    user_node = graph.nodes.match("GAMER", nombre=user_id).first()
    game_node = graph.nodes.match("JUEGO", titulo=game_id).first()
    
    if user_node and game_node:
        relation = Relationship(user_node, "JUEGA", game_node,
                                desde=since,
                                horas_jugadas=hours_played,
                                favorito=favorite)
        
        graph.create(relation)
        return relation
    else:
        print(f"No se encontró el usuario con id {user_id} o el juego con id {game_id}")
        return None

def user_reviewed_game(user_id, review_id, date, rating, recommends):
    user_node = graph.nodes.match("GAMER", nombre=user_id).first()
    review_node = graph.nodes.match("REVIEW", titulo=review_id).first()
    
    if user_node and review_node:
        relation = Relationship(user_node, "RESEÑÓ", review_node,
                                fecha=date,
                                puntuacion=rating,
                                recomienda=recommends)
        
        graph.create(relation)
        return relation
    else:
        print(f"No se encontró el usuario con id {user_id} o la reseña con id {review_id}")
        return None

def review_rates_game(review_id, game_id, date, stars, verified):
    review_node = graph.nodes.match("REVIEW", titulo=review_id).first()
    game_node = graph.nodes.match("JUEGO", titulo=game_id).first()
    
    if review_node and game_node:
        relation = Relationship(review_node, "CALIFICA", game_node,
                                fecha=date,
                                estrellas=stars,
                                verificado=verified)
        
        graph.create(relation)
        return relation
    else:
        print(f"No se encontró la reseña con id {review_id} o el juego con id {game_id}")
        return None

def game_available_on_platform(game_id, platform_id, release_date, digital_format, special_edition):
    game_node = graph.nodes.match("JUEGO", titulo=game_id).first()
    platform_node = graph.nodes.match("PLATAFORMA", nombre=platform_id).first()
    
    if game_node and platform_node:
        relation = Relationship(game_node, "DISPONIBLE_EN", platform_node,
                                fecha_lanzamiento=release_date,
                                formato_digital=digital_format,
                                edicion_especial=special_edition)
        
        graph.create(relation)
        return relation
    else:
        print(f"No se encontró el juego con id {game_id} o la plataforma con id {platform_id}")
        return None

def game_belongs_to_genre(game_id, genre_name, release_date, exclusive, average_rating):
    game_node = graph.nodes.match("JUEGO", titulo=game_id).first()
    genre_node = graph.nodes.match("GENERO", nombre=genre_name).first()
    
    if game_node and genre_node:
        relation = Relationship(game_node, "PERTENECE_A", genre_node,
                                fecha_lanzamiento=release_date,
                                exclusivo=exclusive,
                                calificacion_media=average_rating)
        
        graph.create(relation)
        return relation
    else:
        print(f"No se encontró el juego con id {game_id} o el género con nombre {genre_name}")
        return None

def guide_belongs_to_game(guide_id, game_id, stars):
    guide_node = graph.nodes.match("GUIA", titulo=guide_id).first()
    game_node = graph.nodes.match("JUEGO", titulo=game_id).first()
    
    if guide_node and game_node:
        relation = Relationship(guide_node, "EXPLICA", game_node,
                                estrellas=stars,
                                plataformas=game_node["plataformas"])
        
        graph.create(relation)
        return relation
    else:
        print(f"No se encontró la guía con id {guide_id} o el juego con id {game_id}")
        return None
    
def publisher_publishes_game(publisher_id, game_id, cant_games, territories, fecha_distribucion):
    publisher_node = graph.nodes.match("DISTRIBUIDORA", nombre=publisher_id).first()
    game_node = graph.nodes.match("JUEGO", titulo=game_id).first()
    
    if publisher_node and game_node:
        relation = Relationship(publisher_node, "DISTRIBUYE", game_node,
                                cantidad_distribuida=cant_games,
                                territorios_distribucion=territories,
                                fecha_distribucion=fecha_distribucion)
        
        graph.create(relation)
        return relation
    else:
        print(f'No se encontró la distribuidora con nombre {publisher_id} o el juego con titulo {game_id}')