from graph_tool.all import *
from models import interestGraph

class algorithms:

    def __init__(self):
        pass

    def page_rank(graph: interestGraph):
        pr = graph_tool.centrality.pagerank(graph.g)
        v_name, v_is_user, e_relation = graph.get_graph_properties()

        results = [(v_name[item], pr[item]) for item in graph.g.vertices()]
        results.sort(key = lambda element: element[1], reverse = True)
       
        for item in results:
            print(item)   
      