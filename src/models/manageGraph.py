from graph_tool import *
from models.interestGraph import interestGraph

class manageGraph():

    def save_graph(graph: interestGraph, file_format: str) -> None:
        graph.g.save("data/%s.gt" % graph.get_repo_name())

    def load(load: str) -> Graph:
        return load_graph("data/%s" % load, fmt='gt')
        