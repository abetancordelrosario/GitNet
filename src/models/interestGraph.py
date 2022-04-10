from enum import Enum, auto
from graph_tool.all import *
import requests
import json

class relationship(Enum):
    STARRED = "starred"
    FOLLOWS = "follows"

class interestGraph:
    """
    Creates a interest graph that includes the repository selected, the stargazers
    of this repository, the relationships between them and the starred repositories 
    of each stargazer.

    The constructor requires a dataExtraction object.
    """

    __MAX_REPOS_STARGAZER: int = 20
    __MAX_NUMBER_ITEMS: int = 100
    __API_URL = "https://api.github.com/"


    def __init__(self, full_name_repository: str, token: str) -> None:
        self.g = Graph(directed=True)
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % token
        self.full_name_repository = full_name_repository
        self.set_graph_properties()
        
<<<<<<< Updated upstream
=======
    def extract_data_from_api(self):
        self.__stargazers_starred_repos, self.__stargazers_followers = self.extract_data.fetch_data()
        self.__main_repository = self.extract_data.get_main_repo()
        self.__stargazers = self.extract_data.get_stargazers()
>>>>>>> Stashed changes

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
        
        stargazers: list = self.request_api(None, self.__MAX_NUMBER_ITEMS, "stargazers", True)
        for stargazer in stargazers:
            stargazer_vertex: list = find_vertex(self.g, self.__v_name, stargazer['login'])
            if stargazer_vertex:
                new_stargazer_vertex: Vertex = stargazer_vertex[0]
                self.create_edge(relationship.STARRED, new_stargazer_vertex, main_vertex)
            else:
                new_stargazer_vertex: Vertex = self.create_stargazer_vertex(stargazer)
                self.create_edge(relationship.STARRED, new_stargazer_vertex, main_vertex)

            self.add_follower_relationship(stargazer, new_stargazer_vertex, stargazers)
            self.add_starred_repos(stargazer, new_stargazer_vertex, main_vertex)


    def add_follower_relationship(self, stargazer: json, new_vertex: Vertex, stargazers: list) -> None:
        followers: list = self.request_api(stargazer, self.__MAX_NUMBER_ITEMS, "followers", False)

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

<<<<<<< Updated upstream
    def add_starred_repos(self, stargazer: json, new_vertex: Vertex, main_vertex: Vertex):
        starred_repos: list = self.request_api(stargazer, self.__MAX_REPOS_STARGAZER, "starred", False)
=======

    def add_starred_repos(self, stargazer: json, new_vertex: Vertex, main_vertex: Vertex, index: int):
        starred_repos: list = self.__stargazers_starred_repos[index]
>>>>>>> Stashed changes

        for starred in starred_repos:
            repeated_repos: list = find_vertex(self.g, self.__v_name, starred['name'])
            if repeated_repos:
                if repeated_repos[0] != main_vertex:      
                    self.create_edge(relationship.STARRED, new_vertex, repeated_repos[0])
            else:
                starred_repo: Vertex = self.create_repository_vertex(starred)
                self.create_edge(relationship.STARRED, new_vertex, starred_repo) 
           
    def create_main_vertex(self) -> Vertex:
        main_repo_url: str = self.__API_URL+"repos/%s" % self.full_name_repository
        main_repository = self.session.get(main_repo_url , headers=self.session.headers)
        self.create_repository_vertex(main_repository.json())
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


    def request_api(self, stargazer: json, num_items: int, info: str, is_repo_url: bool) -> list:
        if is_repo_url:
            url: str = self.__API_URL+"repos/%s/%s?per_page=%d" % (self.full_name_repository, info, num_items)
        else:
            url: str = self.__API_URL+"users/%s/%s?per_page=%d" % (stargazer['login'], info, num_items)

        api_response = self.session.get(url , headers=self.session.headers)
        response_json: list = api_response.json()
        if info != "starred":
            while 'next' in api_response.links.keys():
                api_response = requests.get(api_response.links['next']['url'], headers=self.session.headers)
                response_json.extend(api_response.json())

        return response_json

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







      



        



