
from typing import List
from github import Github, GithubException
from graph_tool.all import *
from numpy import ndarray

class createGraph:

    __MAX_REPOS_STARGAZER: int = 500

    def __init__(self, full_name_repository : str, token: str) -> None:
        self.g = Graph()
        self.__client = Github(token, per_page=100)
        self.__repository = self.__client.get_repo(full_name_repository)

    
    def add_nodes_and_edges(self) -> None:
        vertex = self.g.add_vertex()
        v_name : VertexPropertyMap = self.g.new_vertex_property("string")
        v_name[vertex] = self.__repository.name
    
        stargazers: List = self.__repository.get_stargazers()
        for stargazer in stargazers:
            self.g.add_vertex()


    def get_graph_vertices(self) -> ndarray:
        return self.g.get_vertices()

    def get_graph_num_vertices(self) -> int:
        return self.g.num_vertices()


        



