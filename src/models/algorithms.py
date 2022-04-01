import string
from graph_tool.all import *
from models import interestGraph

class algorithms:

    def __init__(self):
        pass

    def get_relevant_users(graph: interestGraph):
        v_name, v_is_user, v_is_repo = graph.get_graph_properties()
        sub_graph = GraphView(graph.g, v_is_user)
        pr = graph_tool.centrality.pagerank(sub_graph)
        results: list = [(v_name[item], pr[item]) for item in sub_graph.vertices()]
 
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant users ***")
        for item in results:
                print(item)   
        print("-----------------------------------------")


    def get_relevant_repos(graph: interestGraph):
        pr = graph_tool.centrality.pagerank(graph.g) 
        v_name, v_is_user, v_is_repo = graph.get_graph_properties()
        
        results: list = [] 
        for item in graph.g.vertices():
            if v_is_repo[item] == 1:
                results.append((v_name[item], pr[item]))
        
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant repos ***")
        for item in results[:10]:
                print(item)   
        print("-----------------------------------------")
        