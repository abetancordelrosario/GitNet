from typing import List
from xmlrpc.client import boolean
from numpy import equal, ndarray
import pytest
import sys
sys.path.insert(0, '..')
from src.models.createGraph import createGraph

"""
Set test example graph.
"""
__token : str = "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"
__full_name_repository : str =  "marius92mc/github-stargazers" 
__test_graph: createGraph = createGraph(__full_name_repository, __token)
__repository_vertices: int = 13
__repository_edges: int = 12



def test_add_vertices_and_edges():
    errors : List = []

    __test_graph.add_vertices_and_edges()
    num_vertices: int = __test_graph.g.num_vertices()  
    num_edges: int = __test_graph.g.num_edges()

    if num_vertices != __repository_vertices:
        errors.append("Incorrect number of vertices") 
    if num_edges != __repository_edges:
        errors.append("Incorrect number of edges") 
    assert not errors, "errors occured:\n{}".format("\n".join(errors))



    


