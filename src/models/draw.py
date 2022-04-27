from graph_tool.all import *

class draw:

    def draw_graph(graph):
        v_name: VertexPropertyMap = graph.get_name()
        graph_draw(graph.g, output="img/graph.pdf")