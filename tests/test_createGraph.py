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
__repository_vertices: int = 233
__repository_edges: int = 238



def test_add_vertices_and_edges():
    errors : List = []

    __test_graph.add_vertices_and_edges()
    num_vertices: int = __test_graph.g.num_vertices()  
    num_edges: int = __test_graph.g.num_edges()
    main_v = __test_graph.g.vertex(0)
    main_v_out: int = main_v.out_degree()
    main_v_in: int = main_v.in_degree()
    print(main_v_out)

    if num_vertices != __repository_vertices:
        errors.append("Incorrect number of vertices") 
    if num_edges != __repository_edges:
        errors.append("Incorrect number of edges") 
    if num_edges != __repository_edges:
        errors.append("Incorrect number of edges")
    if main_v_in != 14 or main_v_out != 0:
        errors.append("Incorrect main vertex degree")
        print(main_v_in)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))



    


