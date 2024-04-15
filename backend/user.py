from crud import *

def find_games_by_genre(genre):
    query = (
        "MATCH (g:VIDEOJUEGO)-[:PERTENECE_A]->(genre:GENERO {nombre: $genre}) "
        'RETURN g.titulo AS Titulo, g.plataformas AS Plataformas, g.lanzamiento AS Fecha_de_Lanzamiento LIMIT 20'
    )
    result = graph.run(query, genre=genre)
    return result

def find_games_by_title(title):
    query = (
        "MATCH (g:VIDEOJUEGO) "
        "WHERE toLower(g.titulo) CONTAINS toLower($title) "
        "RETURN g.titulo AS Titulo, g.plataformas AS Plataformas, g.lanzamiento AS Fecha_de_Lanzamiento LIMIT 20"
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
        "RETURN g.titulo AS Titulo, g.plataformas AS Plataformas, g.lanzamiento AS Fecha_de_Lanzamiento, genre.nombre as Genero, AVG(cal.estrellas) AS Rating "
        "ORDER BY Rating DESC LIMIT 30"
    )
    result = graph.run(query2, user_id=user_id)
    
    return result.data()

def recommend_games_for_user(user_id):
    query1 = (
        "MATCH (u:GAMER {nombre: $user_id})-[:JUEGA]->(g:JUEGO)<-[:JUEGA]-(other:GAMER)-[:JUEGA]->(rec:JUEGO) "
        "WHERE NOT (u)-[:JUEGA]->(rec) "
        "RETURN rec.titulo AS title, rec.plataformas AS platform, rec.lanzamiento AS release_date, COUNT(*) AS score "
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