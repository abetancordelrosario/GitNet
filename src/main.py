from models.createGraph import createGraph
from models.algorithms import algorithms  
import time


def main() -> None:   
    graph = createGraph("marius92mc/github-stargazers","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")
    # graph = createGraph("yavallejo/tallerwordpress","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")
    initialTime = time.time()
    graph.add_vertices_and_edges()
    algorithms.page_rank(graph.g)
    
    # graph.prueba()
    print("Tiempo que tarda en ejecutar el programa:", (time.time() - initialTime), "seconds")
    print(graph.g.num_vertices)

if __name__ == "__main__":
    main()
# 