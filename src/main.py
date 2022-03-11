from models.createGraph import createGraph
from numpy import ndarray


def main() -> None:   
    graph = createGraph("alexisrolland/flask-graphene-sqlalchemy","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")
    graph.add_vertices_and_edges()

if __name__ == "__main__":
    main()
