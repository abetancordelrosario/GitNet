import time
from typing import List
from xmlrpc.client import boolean
from graph_tool.all import *
import requests
import json

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
    __API_URL = "https://api.github.com/"

    __v_name: VertexPropertyMap 
    __v_is_user: VertexPropertyMap 
    __e_relation: EdgePropertyMap 

    def __init__(self, full_name_repository : str, token: str) -> None:
        self.g = Graph()
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % token
        self.full_name_repository = full_name_repository
        self.set_graph_properties()
        

    def set_graph_properties(self) -> None:
        self.__v_name: VertexPropertyMap = self.g.new_vertex_property("string")
        self.__v_is_user: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__e_relation: EdgePropertyMap = self.g.new_edge_property("string")

    def prueba(self):
        # Obtener repositorio
        repositorio = self.session.get(self.__API_URL+"repos/%s" % self.full_name_repository , headers=self.session.headers)

        # Obtener stargazers
        stargazers = self.session.get(self.__API_URL+"repos/%s/stargazers" % self.full_name_repository , headers=self.session.headers)
        for stargazer in stargazers.json():

            followers = self.session.get(self.__API_URL+"users/%s/followers" % stargazer['login'] , headers=self.session.headers)
            
            starred_repos = self.session.get(self.__API_URL+"users/%s/starred" % stargazer['login'] , headers=self.session.headers)
            print(starred_repos)




    def add_vertices_and_edges(self) -> None:
        repository = self.session.get(self.__API_URL+"repos/%s" % self.full_name_repository , headers=self.session.headers)
        self.create_vertex(repository.json() ['name'], self.__IS_REPOSITORY)
        main_vertex: Vertex = self.g.vertex(0)
        
        stargazers = self.session.get(self.__API_URL+"repos/%s/stargazers" % self.full_name_repository , headers=self.session.headers)
        for stargazer in stargazers.json():
            try:
                stargazer_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, stargazer['login'])
                new_stargazer_vertex: Vertex = stargazer_vertex[0]
                self.create_edge("starred", new_stargazer_vertex, main_vertex)
            except:
                new_stargazer_vertex: Vertex = self.create_vertex(stargazer['login'], self.__IS_USER)
                self.create_edge("starred", new_stargazer_vertex, main_vertex)

            
            followers = self.session.get(self.__API_URL+"users/%s/followers" % stargazer['login'] , headers=self.session.headers)
            """for follower in followers.json:
                try:
                    stargazers.index(follower)
                    try:
                        follower_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, follower.login)
                        self.create_edge("starred", follower_vertex[0], new_stargazer_vertex)    
                    except:
                        follower_vertex = self.create_vertex(follower.login, self.__IS_USER)
                        self.create_edge("starred", follower_vertex, new_stargazer_vertex)
                except:
                    pass"""
            print(stargazer['login'])
            starred_repos = self.session.get(self.__API_URL+"users/%s/starred" % stargazer['login'] , headers=self.session.headers)
            for starred in starred_repos.json()[:self.__MAX_REPOS_STARGAZER]:
                repeated_repos: List = graph_tool.util.find_vertex(self.g, self.__v_name, starred['name'])
                try:         
                    if repeated_repos[0] != main_vertex:      
                        self.create_edge("starred", new_stargazer_vertex, repeated_repos[0])
                except:  
                    starred_repo: Vertex = self.create_vertex(starred['name'], self.__IS_REPOSITORY)
                    print(starred['name'])
                    self.create_edge("starred", new_stargazer_vertex, starred_repo) 
            print("--------------------------------------")

                    

    def create_vertex(self, name: str, type: boolean) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_name[vertex] = name
        self.__v_is_user[vertex] = type
        return vertex

    def create_edge(self, relation: str, actual_vertex: Vertex, main_vertex: Vertex) -> None:
        actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
        self.__e_relation[actual_edge] = relation








      



        



