import json
from pickle import FALSE
from typing import List
from xmlrpc.client import boolean
from graph_tool.all import *
import requests

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
        self.g = Graph(directed=True)
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % token
        self.full_name_repository = full_name_repository
        self.set_graph_properties()
        

    def set_graph_properties(self) -> None:
        self.__v_name: VertexPropertyMap = self.g.new_vertex_property("string")
        self.__v_is_user: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__e_relation: EdgePropertyMap = self.g.new_edge_property("string")


    def add_vertices_and_edges(self) -> None:
        repository = self.session.get(self.__API_URL+"repos/%s" % self.full_name_repository , headers=self.session.headers)
        self.create_vertex(repository.json() ['name'], self.__IS_REPOSITORY)
        main_vertex: Vertex = self.g.vertex(0)
        
        stargazers_request = self.session.get(self.__API_URL+"repos/%s/stargazers?per_page=100" % self.full_name_repository , headers=self.session.headers)
        stargazers = [st['login'] for st in stargazers_request.json()]
        for stargazer in stargazers_request.json():
            try:
                stargazer_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, stargazer['login'])
                new_stargazer_vertex: Vertex = stargazer_vertex[0]
                self.create_edge("starred", new_stargazer_vertex, main_vertex)
            except:
                new_stargazer_vertex: Vertex = self.create_vertex(stargazer['login'], self.__IS_USER)
                self.create_edge("starred", new_stargazer_vertex, main_vertex)

            self.add_followers(stargazers, stargazer, new_stargazer_vertex)
            self.add_starred_repos(stargazer, new_stargazer_vertex, main_vertex)


    def add_followers(self, stargazers: List, stargazer: json, new_vertex: Vertex) -> None:
        user_followers_url = self.__API_URL+"users/%s/followers?per_page=100" % stargazer['login']
        response = self.session.get(user_followers_url , headers=self.session.headers)
        followers = response.json()

        while 'next' in response.links.keys():
            response = requests.get(response.links['next']['url'], headers=self.session.headers)
            followers.extend(response.json())

        for follower in followers:
            try:
                stargazers.index(follower['login'])
                try:
                    follower_vertex: List = graph_tool.util.find_vertex(self.g, self.__v_name, follower['login'])
                    self.create_edge("starred", follower_vertex[0], new_vertex)  
                except:
                    follower_vertex = self.create_vertex(follower['login'], self.__IS_USER)
                    self.create_edge("starred", follower_vertex, new_vertex)
            except:
                    pass

    def add_starred_repos(self, stargazer: json, new_vertex: Vertex, main_vertex: Vertex):
        starred_repos = self.session.get(self.__API_URL+"users/%s/starred" % stargazer['login'] , headers=self.session.headers)
        
        for starred in starred_repos.json()[:self.__MAX_REPOS_STARGAZER]:
            repeated_repos: List = graph_tool.util.find_vertex(self.g, self.__v_name, starred['name'])
            try:         
                if repeated_repos[0] != main_vertex:      
                    self.create_edge("starred", new_vertex, repeated_repos[0])
            except:  
                starred_repo: Vertex = self.create_vertex(starred['name'], self.__IS_REPOSITORY)
                self.create_edge("starred", new_vertex, starred_repo) 
           
    
    def create_vertex(self, name: str, type: boolean) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_name[vertex] = name
        self.__v_is_user[vertex] = type
        return vertex

    def create_edge(self, relation: str, actual_vertex: Vertex, main_vertex: Vertex) -> None:
        actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
        self.__e_relation[actual_edge] = relation




      



        



