from graph_tool.all import *

class draw:

    def draw_graph(graph) -> None:
        graph_draw(graph.g, output="img/graph.pdf")