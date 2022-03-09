
from typing import List
from github import Github, GithubException
from graph_tool.all import *

class createGraph:

    __MAX_REPOS_STARGAZER: int = 500

    def __init__(self, full_name_repository : str, token: str) -> None:
        self.g = Graph()
        self.__client = Github(token, per_page=100)
        self.__repository = self.__client.get_repo(full_name_repository)

    def __init__():
        pass

    
    def add_nodes_and_edges(self):
        self.g.add_vertex()
        v_name = self.g.new_vertex_property("string")
        stargazers: List = self.__repository.get_stargazers()
        return 2
        



