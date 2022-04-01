import json
from pickle import FALSE
from typing import List, Tuple
from urllib import response
from xmlrpc.client import boolean
from graph_tool.all import *
import requests

class interestGraph:
    """
    Creates a interest graph that includes the repository selected, the stargazers
    of this repository, the relationships between them and the starred repositories 
    of each stargazer.

    The construtor requires two strings, first is the full repository name 
    (author/repository) and the second one is the user's GitHub token.
    """

    __MAX_REPOS_STARGAZER: int = 20
    __MAX_NUMBER_ITEMS: int = 100
    __IS_USER: boolean = True
    __IS_REPOSITORY: boolean = False
    __API_URL = "https://api.github.com/"

    __v_name: VertexPropertyMap 
    __v_is_user: VertexPropertyMap 
    __v_is_repo: VertexPropertyMap 
    __e_relation: EdgePropertyMap 

    def __init__(self, full_name_repository: str, token: str) -> None:
        self.g = Graph(directed=True)
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % token
        self.full_name_repository = full_name_repository
        self.set_graph_properties()
        

    def set_graph_properties(self) -> None:
        self.__v_name: VertexPropertyMap = self.g.new_vertex_property("string")
        self.__v_is_user: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__v_is_repo: VertexPropertyMap = self.g.new_vertex_property("bool") 
        self.__e_relation: EdgePropertyMap = self.g.new_edge_property("string")


    def create_graph(self) -> None:
        main_vertex: Vertex = self.create_main_vertex()
        
        stargazers: list = self.request_api(None, self.__MAX_NUMBER_ITEMS, "stargazers", True)
        for stargazer in stargazers:
            try:
                #If the vertex already exists.
                stargazer_vertex: List = find_vertex(self.g, self.__v_name, stargazer['login'])
                new_stargazer_vertex: Vertex = stargazer_vertex[0]
                self.create_edge("starred", new_stargazer_vertex, main_vertex)
            except:
                new_stargazer_vertex: Vertex = self.create_vertex(stargazer['login'], self.__IS_USER)
                self.create_edge("starred", new_stargazer_vertex, main_vertex)

            self.add_follower_relationship(stargazer, new_stargazer_vertex, stargazers)
            self.add_starred_repos(stargazer, new_stargazer_vertex, main_vertex)


    def add_follower_relationship(self, stargazer: json, new_vertex: Vertex, stargazers: list) -> None:
        followers: list = self.request_api(stargazer, self.__MAX_NUMBER_ITEMS, "followers", False)

        for follower in followers:
            try:
                stargazers.index(follower)
                try:
                    # If the follower vertex already exists
                    follower_vertex: List = find_vertex(self.g, self.__v_name, follower['login'])
                    self.create_edge("follows", follower_vertex[0], new_vertex)  
                except:
                    follower_vertex = self.create_vertex(follower['login'], self.__IS_USER)
                    self.create_edge("follows", follower_vertex, new_vertex)
            except:
                    pass

    def add_starred_repos(self, stargazer: json, new_vertex: Vertex, main_vertex: Vertex):
        starred_repos: list = self.request_api(stargazer, self.__MAX_REPOS_STARGAZER, "starred", False)

        for starred in starred_repos:
            repeated_repos: List = find_vertex(self.g, self.__v_name, starred['name'])
            try:  
                # If repo vertex already exists and is not the main vertex    
                if repeated_repos[0] != main_vertex:      
                    self.create_edge("starred", new_vertex, repeated_repos[0])
            except:  
                starred_repo: Vertex = self.create_vertex(starred['name'], self.__IS_REPOSITORY)
                self.create_edge("starred", new_vertex, starred_repo) 
           
    def create_main_vertex(self) -> Vertex:
        main_repo_url: str = self.__API_URL+"repos/%s" % self.full_name_repository
        main_repository: response = self.session.get(main_repo_url , headers=self.session.headers)
        self.create_vertex(main_repository.json() ['name'], self.__IS_REPOSITORY)
        main_vertex: Vertex = self.g.vertex(0)
        return main_vertex
        

    def create_vertex(self, name: str, type: boolean) -> Vertex:
        vertex = self.g.add_vertex()
        self.__v_name[vertex] = name
        if type == self.__IS_USER:
            self.__v_is_user[vertex] = True
        else:
            self.__v_is_repo[vertex] = True 
        return vertex

    def create_edge(self, relation: str, actual_vertex: Vertex, main_vertex: Vertex) -> None:
        actual_edge: Edge = self.g.add_edge(actual_vertex,main_vertex)
        self.__e_relation[actual_edge] = relation


    def request_api(self, stargazer: json, num_items: int, info: str, is_repo_url: boolean) -> list:
        if is_repo_url:
            url: str = self.__API_URL+"repos/%s/%s?per_page=%d" % (self.full_name_repository, info, num_items)
        else:
            url: str = self.__API_URL+"users/%s/%s?per_page=%d" % (stargazer['login'], info, num_items)

        api_response = response = self.session.get(url , headers=self.session.headers)
        response_json: list = api_response.json()
        if info != "starred":
            while 'next' in api_response.links.keys():
                api_response: response = requests.get(api_response.links['next']['url'], headers=self.session.headers)
                response_json.extend(api_response.json())

        return response_json


    def get_graph_properties(self) -> list:
        return [self.__v_name, self.__v_is_user, self.__v_is_repo]





      



        



