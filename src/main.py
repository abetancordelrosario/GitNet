from models.createGraph import createGraph
from numpy import ndarray
import time


def main() -> None:   
    #graph = createGraph("alexisrolland/flask-graphene-sqlalchemy","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")
    graph = createGraph("marius92mc/github-stargazers","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")
    #graph = createGraph("jmportilla/Python-for-Algorithms--Data-Structures--and-Interviews","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")
    #graph = createGraph("yavallejo/tallerwordpress","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")
    #graph = createGraph("Nurmuhammad0071/asosiy_xampp","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")
    initialTime = time.time()
    graph.add_vertices_and_edges()
    print("Tiempo que tarda en ejecutar el programa:", (time.time() - initialTime), "seconds")
    print(graph.g.num_vertices)

if __name__ == "__main__":
    main()
