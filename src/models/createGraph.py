import time
from typing import List
from xmlrpc.client import boolean
from github import Github
from graph_tool.all import *

class createGraph:
    """
    Creates a interest graph that includes the repository selected, the stargazers
    of this repository and the starred repositories of each stargazer.

    The construtor requires two strings, first is the full repository name 
    (author/repository) and the second one is the user's GitHub token.
    """

    __MAX_REPOS_STARGAZER: int = 20
    __IS_USER: boolean = True
    __IS_REPOSITORY: boolean = False
    __OPENMP_THREADS: int = 16

    __v_name: VertexPropertyMap 
    __v_is_user: VertexPropertyMap 
    __e_relation: EdgePropertyMap 

    def __init__(self, full_name_repository : str, token: str) -> None:
        self.g = Graph()
        self.__client = Github(token, per_page=100)
        self.__repository = self.__client.get_repo(full_name_repository)
        graph_tool.openmp_set_num_threads(self.__OPENMP_THREADS)
        self.set_graph_properties()
        

    def set_graph_properties(self) -> None:
        self.__v_name: VertexPropertyMap = self.g.new_vertex_property("string")
        self.__v_is_user: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__e_relation: EdgePropertyMap = self.g.new_edge_property("string")
    
    def add_vertices_and_edges(self) -> None:
        self.create_vertex(self.__repository.name, self.__IS_REPOSITORY)
        main_vertex: Vertex = self.g.vertex(0)
        
        stargazers: List = [sg for sg in self.__repository.get_stargazers()]
        for stargazer in stargazers:
            try:
                stargazer_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, stargazer.login)
                new_stargazer_vertex: Vertex = stargazer_vertex[0]
                self.create_edge("starred", new_stargazer_vertex, main_vertex)
            except:
                new_stargazer_vertex: Vertex = self.create_vertex(stargazer.login, self.__IS_USER)
                self.create_edge("starred", new_stargazer_vertex, main_vertex)

            for follower in stargazer.get_followers():
                try:
                    stargazers.index(follower)
                    try:
                        follower_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, follower.login)
                        self.create_edge("starred", follower_vertex[0], new_stargazer_vertex)    
                    except:
                        follower_vertex = self.create_vertex(follower.login, self.__IS_USER)
                        self.create_edge("starred", follower_vertex, new_stargazer_vertex)
                except:
                    pass


            for starred in stargazer.get_starred()[:self.__MAX_REPOS_STARGAZER]:
                repeated_repos: List = graph_tool.util.find_vertex(self.g, self.__v_name, starred.name)
                try:         
                    if repeated_repos[0] != main_vertex:      
                        self.create_edge("starred", new_stargazer_vertex, repeated_repos[0])
                except:  
                    starred_repo: Vertex = self.create_vertex(starred.name, self.__IS_REPOSITORY)
                    self.create_edge("starred", new_stargazer_vertex, starred_repo) 

                    

    def create_vertex(self, name: str, type: boolean) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_name[vertex] = name
        self.__v_is_user[vertex] = type
        return vertex

    def create_edge(self, relation: str, actual_vertex: Vertex, main_vertex: Vertex) -> None:
        actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
        self.__e_relation[actual_edge] = relation








      



        



