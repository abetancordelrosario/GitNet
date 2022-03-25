from graph_tool.all import *

class algorithms:

    def __init__(self):
        pass

    def page_rank(g: Graph):
        pr = graph_tool.centrality.pagerank(g)

        results = [(item, pr[item]) for item in g.vertices()]
        results.sort(key = lambda element: element[1], reverse = True)
       
        for item in results:
            print(item)   
      