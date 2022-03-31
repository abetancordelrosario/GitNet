from graph_tool.all import *

class draw:

    def __init__(self):
        pass


    def draw_graph(graph):
        v_name, v_is_user, v_is_repo = graph.get_graph_properties()
        graph_draw(graph.g, vertex_font_size=2, vertex_text=v_name, output="graph.pdf")