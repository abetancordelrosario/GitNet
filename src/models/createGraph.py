from typing import List
from xmlrpc.client import boolean
from github import Github, GithubException
from graph_tool.all import *

class createGraph:
    """
    Creates a interest graph that includes the repository selected, the stargazers
    of this repository and the stars of each stargazer.

    The construtor requires a two strings one the first is the full repository name 
    (author/repository) and the second one is the user's token.
    """

    __MAX_REPOS_STARGAZER: int = 500
    __IS_USER: boolean = True
    __IS_REPOSITORY: boolean = False

    def __init__(self, full_name_repository : str, token: str) -> None:
        self.g = Graph()
        self.__client = Github(token, per_page=100)
        self.__repository = self.__client.get_repo(full_name_repository)
        self.__v_name: VertexPropertyMap = self.g.new_vertex_property("string")
        self.__v_is_user: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__e_relation: EdgePropertyMap = self.g.new_edge_property("string")

    
    def add_vertices_and_edges(self) -> None:
        self.create_vertex(self.__repository.name, self.__IS_REPOSITORY)
        main_vertex: Vertex = self.g.vertex(0)

        stargazers: List = self.__repository.get_stargazers()
        for index, stargazer in enumerate(stargazers):
            self.create_vertex(stargazer.name, self.__IS_USER)
            actual_vertex: Vertex = self.g.vertex(index + 1)
            actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
            self.__e_relation[actual_edge] = "stars"

    def create_vertex(self, name: str, type: boolean):
        vertex = self.g.add_vertex()
        self.__v_name[vertex] = name
        self.__v_is_user[vertex] = type




        



