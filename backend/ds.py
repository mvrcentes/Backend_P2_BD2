from py2neo import Graph
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from database import *  # Asumiendo que aquí está tu conexión a la base de datos

# Exportar el grafo de Neo4j a NetworkX
query = """
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100  // Limitar los resultados a los primeros 1000 nodos
"""
result = graph.run(query)
G = nx.Graph()

for record in result:
    n_props = record['n'].keys()  # Obtener las propiedades del nodo n
    m_props = record['m'].keys()  # Obtener las propiedades del nodo m
    
    # Verificar si las propiedades 'titulo' y 'nombre' existen en los nodos
    if 'titulo' in n_props and 'nombre' in m_props:
        G.add_node(record['n']['titulo'])
        G.add_node(record['m']['nombre'])
        G.add_edge(record['n']['titulo'], record['m']['nombre'])
    else:
        print("Los nodos no tienen las propiedades necesarias:", record['n'], record['m'])

# Encuentra las comunidades utilizando el algoritmo de Louvain
communities = list(greedy_modularity_communities(G))

# Imprime las comunidades encontradas
for i, community in enumerate(communities):
    print(f"Comunidad {i + 1}: {community}")
