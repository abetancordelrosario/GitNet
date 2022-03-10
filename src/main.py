from models.createGraph import createGraph
from numpy import ndarray


def main() -> None:   
    graph = createGraph()
    graph.add_nodes_and_edges()

if __name__ == "__main__":
    main()
