import pytest
from src.models.createGraph import createGraph

class test_createGraph:

    test_graph = createGraph()

    def test(self):
        assert 2 == self.test_graph.add_nodes_and_edges()

