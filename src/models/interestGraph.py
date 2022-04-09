from enum import Enum
from graph_tool.all import *
import json
from models.dataExtraction import dataExtraction

class relationship(Enum):
    STARRED = "starred"
    FOLLOWS = "follows"

class interestGraph:
    """
    Creates a interest graph that includes the repository selected, the stargazers
    of this repository, the relationships between them and the starred repositories 
    of each stargazer.

    The construtor requires two strings, first is the full repository name 
    (author/repository) and the second one is the user's GitHub token.
    """
    
    __main_repository: json 
    __stargazers = list = []
    __stargazers_starred_repos: list = []
    __stargazers_followers: list = []

    def __init__(self, full_name_repository: str, token: str) -> None:
        self.g = Graph(directed=True)
        self.full_name_repository = full_name_repository
        self.token = token
        self.extract_data_from_api()
        self.set_graph_properties()
        
    def extract_data_from_api(self):
        extract_data = dataExtraction(self.full_name_repository, self.token)
        self.__stargazers_starred_repos, self.__stargazers_followers = extract_data.foo()
        self.__main_repository = extract_data.get_main_repo()
        self.__stargazers = extract_data.get_stargazers()

    def set_graph_properties(self) -> None:
        self.__v_name: VertexPropertyMap = self.g.new_vertex_property("string")
        self.__v_is_user: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__v_is_repo: VertexPropertyMap = self.g.new_vertex_property("bool")
        self.__v_repo_st: VertexPropertyMap = self.g.new_vertex_property("int32_t")
        self.__v_repo_forks: VertexPropertyMap = self.g.new_vertex_property("int32_t") 
        self.__v_repo_date: VertexPropertyMap = self.g.new_vertex_property("string") 
        self.__v_repo_lang: VertexPropertyMap = self.g.new_vertex_property("string") 
        self.__e_relation: EdgePropertyMap = self.g.new_edge_property("string")


    def create_graph(self) -> None:
        main_vertex: Vertex = self.create_main_vertex()

        for index, stargazer in enumerate(self.__stargazers):
            stargazer_vertex: list = find_vertex(self.g, self.__v_name, stargazer['login'])
            if stargazer_vertex:
                new_stargazer_vertex: Vertex = stargazer_vertex[0]
                self.create_edge(relationship.STARRED, new_stargazer_vertex, main_vertex)
            else:
                new_stargazer_vertex: Vertex = self.create_stargazer_vertex(stargazer)
                self.create_edge(relationship.STARRED, new_stargazer_vertex, main_vertex)

            self.add_follower_relationship(stargazer, new_stargazer_vertex, self.__stargazers, index)
            self.add_starred_repos(stargazer, new_stargazer_vertex, main_vertex, index)


    def add_follower_relationship(self, stargazer: json, new_vertex: Vertex, stargazers: list, index: int) -> None:
        followers: list = self.__stargazers_followers[index]

        for follower in followers:
            try:
                stargazers.index(follower)
                follower_vertex: list = find_vertex(self.g, self.__v_name, follower['login'])
                if follower_vertex:
                    self.create_edge(relationship.FOLLOWS, follower_vertex[0], new_vertex)  
                else:
                    follower_vertex = self.create_stargazer_vertex(follower)
                    self.create_edge(relationship.FOLLOWS, follower_vertex, new_vertex)
            except:
                    pass

    def add_starred_repos(self, stargazer: json, new_vertex: Vertex, main_vertex: Vertex, index: int):
        starred_repos: list = self.__stargazers_starred_repos[index]

        for starred in starred_repos:
            repeated_repos: list = find_vertex(self.g, self.__v_name, starred['name'])
            if repeated_repos:
                if repeated_repos[0] != main_vertex:      
                    self.create_edge(relationship.STARRED, new_vertex, repeated_repos[0])
            else:
                starred_repo: Vertex = self.create_repository_vertex(starred)
                self.create_edge(relationship.STARRED, new_vertex, starred_repo) 
           
    def create_main_vertex(self) -> Vertex:
        self.create_repository_vertex(self.__main_repository)
        main_vertex: Vertex = self.g.vertex(0)
        return main_vertex
        

    def create_stargazer_vertex(self, vertex_info: json) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_is_user[vertex] = True
        self.__v_name[vertex] = vertex_info['login']
        return vertex

    
    def create_repository_vertex(self, vertex_info: json) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_is_repo[vertex] = True 
        self.__v_name[vertex] = vertex_info['name']
        self.__v_repo_st[vertex] = vertex_info['stargazers_count']
        self.__v_repo_lang[vertex] = vertex_info['language'] 
        self.__v_repo_forks[vertex] = vertex_info['forks_count']
        self.__v_repo_date[vertex] = vertex_info['created_at']
        return vertex


    def create_edge(self, relation: str, actual_vertex: Vertex, main_vertex: Vertex) -> None:
        actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
        self.__e_relation[actual_edge] = relation


    def get_name(self) -> VertexPropertyMap:
        return self.__v_name

    def get_is_user(self) -> VertexPropertyMap:
        return self.__v_is_user

    def get_is_repo(self) -> VertexPropertyMap:
        return self.__v_is_repo

    def get_repo_st(self) -> VertexPropertyMap:
        return self.__v_repo_st

    def get_repo_lang(self) -> VertexPropertyMap:
        return self.__v_repo_lang

    def get_repo_forks(self) -> VertexPropertyMap:
        return self.__v_repo_forks

    def get_repo_date(self) -> VertexPropertyMap:
        return self.__v_repo_date







      



        



