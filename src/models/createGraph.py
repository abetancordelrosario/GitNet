from typing import List
from warnings import catch_warnings
from xmlrpc.client import boolean
from github import Github, GithubException
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
        
        stargazers: List = [sg for sg in self.__repository.get_stargazers()]
        for stargazer in stargazers:
            try:
                stargazer_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, starred.name)
                self.create_edge("starred", stargazer_vertex, main_vertex)
            except:
                new_stargazer_vertex: Vertex = self.create_vertex(stargazer.login, self.__IS_USER)
                self.create_edge("starred", new_stargazer_vertex, main_vertex)
        
            for follower in stargazer.get_followers():
                try:
                    index =  stargazers.index(follower)
                    try:
                        follower_vertex: Vertex = self.g.vertex(index)
                        self.create_edge("starred", follower_vertex, new_stargazer_vertex)    
                    except:
                        follower_vertex = self.create_vertex(follower.login, self.__IS_USER)
                        self.create_edge("starred", follower_vertex, new_stargazer_vertex)
                except:
                    pass

            for starred in stargazer.get_starred()[:self.__MAX_REPOS_STARGAZER]:
                repeated_repos: List = graph_tool.util.find_vertex(self.g, self.__v_name, starred.name)
                try:         
                    self.create_edge("starred", new_stargazer_vertex, repeated_repos[0])
                except:  
                    starred_repo: Vertex = self.create_vertex(starred.name, self.__IS_REPOSITORY)
                    self.create_edge("starred", new_stargazer_vertex, starred_repo) 
        
        marius: List = graph_tool.util.find_vertex(self.g, self.__v_name, "abetancordelrosario")
        m = marius[0]
        print(m.in_degree())
        print(m.out_degree())

    def create_vertex(self, name: str, type: boolean) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_name[vertex] = name
        self.__v_is_user[vertex] = type
        return vertex

    def create_edge(self, relation: str, actual_vertex: Vertex, main_vertex: Vertex) -> None:
        actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
        self.__e_relation[actual_edge] = relation








      



        



