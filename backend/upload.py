from database import graph
import csv
import time
import ast

# Conectar a la base de datos de Neo4j

def main():
    f = 'video_games.csv'
    
    with open(f, 'r+') as in_file:
        reader = csv.reader(in_file, delimiter=',')
        next(reader, None)        
        batch = graph.begin()                           

        try:
            print("Processing file...")
            i = 0
            j = 0
            for row in reader:    
                if row:
                    print(row)
                    # Convertir la cadena de plataformas a lista
                    plataformas = ast.literal_eval(row[3])
                    
                    params = {
                        "a": row[0],  
                        "b": row[1],  
                        "c": row[2],  
                        "d": plataformas,  
                        "e": row[4],  
                        "f": row[5],  
                        "g": row[6],  
                        "h": row[7],  
                        "i": row[8],  
                    }

                    # Crear nodo con labels VIDEOJUEGO y JUEGO
                    query_nodo = """
                        MERGE (n:VIDEOJUEGO:JUEGO {titulo: $a, precio: $b, lanzamiento: $c, plataformas: $d, multijugador: $e})
                    """
                    batch.run(query_nodo, params)

                    # Crear relación PERTENECE_A
                    query_relacion = """
                        MATCH (n:VIDEOJUEGO {titulo: $a})
                        MATCH (g:GENERO {nombre: $f})
                        MERGE (n)-[r:PERTENECE_A {fecha_lanzamiento: $g, exclusivo: $h, calificacion_media: $i}]->(g)
                    """
                    batch.run(query_relacion, params)

                    i += 1
                    j += 1

                    if i == 1000:
                        graph.commit(batch)
                        print(j, "lines processed")
                        i = 0
                        batch = graph.begin()

            else:
                graph.commit(batch)
                print(j, "lines processed")    

        except Exception as e:
            print(e, row, reader.line_num)

def strip(string): 
    return ''.join([c if 0 < ord(c) < 128 else ' ' for c in string]) 

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print("Time to complete:", end)