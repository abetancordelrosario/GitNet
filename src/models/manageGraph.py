from models.interestGraph import interestGraph

class manageGraph():

    def save_graph(graph: interestGraph, file_format: str) -> None:
        graph.g.save("data/%s" % graph.get_repo_name(), file_format)

    
        