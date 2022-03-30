import string
from unittest import result
from graph_tool.all import *
from models import interestGraph

class algorithms:

    def __init__(self):
        pass

    def page_rank(graph: interestGraph, type: string):
        v_name, v_is_user, v_is_repo = graph.get_graph_properties()
        if type == "user":
            sub_graph = GraphView(graph.g, v_is_user)
            pr = graph_tool.centrality.pagerank(sub_graph)
            results: list = [(v_name[item], pr[item]) for item in sub_graph.vertices()]
        elif type == "repo":
            sub_graph = graph.g
            results: list = [] 
            pr = graph_tool.centrality.pagerank(sub_graph) 
            for item in sub_graph.vertices():
                if v_is_repo[item] == 1:
                    results.append((v_name[item], pr[item]))
        

        results.sort(key = lambda element: element[1], reverse = True)
       
        
        for item in results:
                print(item)   


    