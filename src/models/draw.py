from graph_tool.all import *

class draw:

    def __init__(self):
        pass


    def draw_graph(graph):
        graph_properties = graph.get_graph_properties()
        v_name: VertexPropertyMap = graph_properties[0]
        # graph_draw(graph.g, vertex_font_size=2, vertex_text=v_name, output="graph.pdf")
        graph_draw(graph.g, output="graph.pdf")