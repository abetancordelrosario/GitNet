from models.createGraph import createGraph
from numpy import ndarray


def main() -> None:   
    graph = createGraph("marius92mc/github-stargazers","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")
    graph.add_vertices_and_edges()

if __name__ == "__main__":
    main()
