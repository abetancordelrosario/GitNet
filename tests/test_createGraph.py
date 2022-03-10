from typing import List
from numpy import ndarray
import sys
sys.path.insert(0, '..')
from src.models.createGraph import createGraph


#Set test example graph.
__token : str = "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"
__full_name_repository : str =  "marius92mc/github-stargazers" 
__test_graph = createGraph(__full_name_repository, __token)
__repository_vertices = 13


def test_add_nodes_and_edges():
    errors : List = []

    __test_graph.add_nodes_and_edges()
    num_vertices : ndarray = __test_graph.get_graph_num_vertices()

    if num_vertices != __repository_vertices:
        errors.append("Incorrect number of vertives")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


