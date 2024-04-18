from crud import *

def find_games_by_genre(genre):
    query = (
        "MATCH (g:VIDEOJUEGO)-[:PERTENECE_A]->(genre:GENERO {nombre: $genre}) "
        'RETURN g.titulo AS Titulo, g.clasificacion as Clasificacion, g.lanzamiento AS Fecha_de_Lanzamiento LIMIT 20'
    )
    result = graph.run(query, genre=genre)
    return result

def find_games_by_title(title):
    query = (
        "MATCH (g:VIDEOJUEGO) "
        "WHERE toLower(g.titulo) CONTAINS toLower($title) "
        "RETURN g.titulo AS Titulo, g.clasificacion as Clasificacion, g.lanzamiento AS Fecha_de_Lanzamiento LIMIT 20"
    )
    result = graph.run(query, title=title)
    return result

def recommend_games_for_user_genres(user_id):   
    query2 = (
        "MATCH (u:GAMER {nombre: $user_id}) "
        "UNWIND u.generos_favoritos AS fav_genre "
        "MATCH (g:JUEGO)-[:PERTENECE_A]->(genre:GENERO {nombre: fav_genre}) "
        "WITH g, genre "
        "MATCH (r:REVIEW)-[cal:CALIFICA]->(g) "
        "WHERE cal.estrellas >= 3 "
        "RETURN g.titulo AS Titulo, g.clasificacion as Clasificacion, g.lanzamiento AS Fecha_de_Lanzamiento, genre.nombre as Genero, AVG(cal.estrellas) AS Rating "
        "ORDER BY Rating DESC LIMIT 30"
    )
    result = graph.run(query2, user_id=user_id)
    
    return result.data()

def recommend_games_for_user(user_id):
    query1 = (
        "MATCH (u:GAMER {nombre: $user_id})-[:JUEGA]->(g:JUEGO)<-[:JUEGA]-(other:GAMER)-[:JUEGA]->(rec:JUEGO) "
        "WHERE NOT (u)-[:JUEGA]->(rec) "
        "RETURN rec.titulo AS title, rec.clasificacion AS clasificacion, rec.lanzamiento AS release_date, COUNT(*) AS score "
        "ORDER BY score DESC LIMIT 30 "
    )
    result = graph.run(query1, user_id=user_id)
    
    return result.data()

def create_user_Main():
    user_properties = {
        "nombre": str,
        "edad": int,
        "email": str,
        "activo": bool,
        "generos_favoritos": list
    }
    user_data = request_data(user_properties)
    created_new_user = merge_node(["USUARIO", "GAMER"], "email", user_data["email"], **user_data)
    
    if created_new_user:
        return True
    else:
        return False
    
def get_user_reviews(user_name):
    query = (
        "MATCH (u:USUARIO {nombre: $user_name})-[r1:`RESEÑÓ`]->(review:REVIEW)-[r2:CALIFICA]->(entity) "
        "RETURN u, r1, review, r2, entity;"
    )
    results = graph.run(query, user_name=user_name).data()
    
    if results:
        for record in results:
            user = record['u']
            review_relation = record['r1']
            review = record['review']
            califica_relation = record['r2']
            entity = record['entity']
            
            print("-" * 50)
            print(f"Usuario: {user['nombre']}")
            print(f"Fecha de la reseña: {review_relation['fecha']}")
            print(f"Título de la reseña: {review['titulo']}")
            print(f"Contenido de la reseña: {review['contenido']}")
            print(f"Calificación: {califica_relation['estrellas']} estrellas")
            print(f"Entidad calificada: {entity.labels}: {entity['titulo'] if 'titulo' in entity else entity['nombre']}")
            print("-" * 50)
    else:
        print("El usuario no tiene reseñas.")

def get_user_games(user_name):
    query = (
        "MATCH (j:GAMER {email: $user_name})-[r:JUEGA]->(g:JUEGO) "
        "RETURN g.titulo as Titulo, r.horas_jugadas as Horas, r.desde as Jugado_Desde "
    )
    results = graph.run(query, user_name=user_name).data()

    return results

def check_entity_exists(entity_type, entity_id):
    if entity_type not in ["JUEGO", "GUIA", "REVIEW"]:
        entity_key = "nombre"
    else:
        entity_key = "titulo"
        
    query = f"MATCH (e:{entity_type} {{{entity_key}: $entity_id}}) RETURN e"
    result = graph.run(query, entity_id=entity_id).data()
    
    if result:
        return True
    else:
        return False
    
def most_popular_games_by_genre():
    query = (
        "MATCH (g:JUEGO)-[:PERTENECE_A]->(genre:GENERO) "
        "MATCH (r:REVIEW)-[:CALIFICA]->(g) "
        "RETURN genre.nombre AS Genero, g.titulo AS Titulo, COUNT(r) AS Numero_de_Reseñas "
        "ORDER BY Numero_de_Reseñas DESC LIMIT 10"
    )
    result = graph.run(query)
    return result.data()

def top_rated_games_overall():
    query = (
        "MATCH (g:JUEGO)<-[:CALIFICA]-(r:REVIEW) "
        "RETURN g.titulo AS Titulo, g.clasificacion as Clasificacion "
        "LIMIT 10"
    )
    result = graph.run(query)
    return result.data()

def most_active_gamers():
    query = (
        "MATCH (g:GAMER)-[r:JUEGA]->(j:JUEGO) "
        "RETURN g.nombre AS Gamer, SUM(r.horas_jugadas) AS Horas_Totales "
        "ORDER BY Horas_Totales DESC LIMIT 10"
    )
    result = graph.run(query)
    return result.data()
