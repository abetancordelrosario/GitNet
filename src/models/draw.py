from graph_tool.all import *

class draw:
    '''
    Draw the graph and save it in pdf format.
    '''

    def draw_graph(graph) -> None:
        graph_draw(graph.g, output="img/graph.pdf")