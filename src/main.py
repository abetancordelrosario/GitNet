from models.draw import draw
from models.interestGraph import interestGraph
from models.algorithms import algorithms  
import time


def command_line() -> None:
    pass

def main() -> None:   
    graph = interestGraph("marius92mc/github-stargazers","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")
    # graph = createGraph("yavallejo/tallerwordpress","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")
    initialTime = time.time()
    graph.create_graph()
    
    algorithms.page_rank(graph, "user")
    # draw.draw_graph(graph)
    
    # graph.prueba()
    print("Tiempo que tarda en ejecutar el programa:", (time.time() - initialTime), "seconds")
    print(graph.g.num_vertices)

if __name__ == "__main__":
    main()
