from database import graph
from py2neo import Graph, NodeMatcher
import csv
import time

print(graph)

def main():
    f = '/Users/mvrcentes/Downloads/video_games.csv'
    
    with open(f, 'r+') as in_file:
        reader = csv.reader(in_file, delimiter=',')
        next(reader, None)        
        batch = graph.begin()                           

        try:
            i = 0
            j = 0
            for row in reader:    
                if row:
                    params = {
                        "a": row[0],  # Title
                        "b": row[1],  # Features.Handheld?
                        "c": row[2],  # Features.Max Players
                        "d": row[3],  # Features.Multiplatform?
                        "e": row[4],  # Features.Online?
                        "f": row[5],  # Metadata.Genres
                        "g": row[6],  # Metadata.Licensed?
                        "h": row[7],  # Metadata.Publishers
                        "i": row[8],  # Metadata.Sequel?
                        "j": row[9],  # Metrics.Review Score
                        "k": row[10], # Metrics.Sales
                        "l": row[11], # Metrics.Used Price
                        "m": row[12], # Release.Console
                        "n": row[13], # Release.Rating
                        "o": row[14], # Release.Re-release?
                        "p": row[15]  # Release.Year
                    }

                    query = """
                        MERGE (game:VIDEOJUEGO {Title: $a, Features_Handheld: $b, Features_Max_Players: $c, Features_Multiplatform: $d, Features_Online: $e,
                        Metadata_Genres: $f, Metadata_Licensed: $g, Metadata_Publishers: $h, Metadata_Sequel: $i, Metrics_Review_Score: $j,
                        Metrics_Sales: $k, Metrics_Used_Price: $l, Release_Console: $m, Release_Rating: $n, Release_Re_release: $o, Release_Year: $p})
                    """

                    batch.run(query, params)
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
    return ''.join([c if 0 < ord(c) < 128 else ' ' for c in string]) #removes non utf-8 chars from string within cell

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print("Time to complete:", end)
