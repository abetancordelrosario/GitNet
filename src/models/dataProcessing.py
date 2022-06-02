from itertools import islice
from datetime import date, timedelta
from graph_tool.all import *

from models import interestGraph


class dataProcessing:

    def __init__(self, graph: interestGraph) -> None:
        self.graph = graph

    def get_relevant_users(self) -> list:
        v_name: VertexPropertyMap = self.graph.get_name()
        v_is_user: VertexPropertyMap = self.graph.get_is_user()
        sub_graph = GraphView(self.graph.g, v_is_user)
        
        pr = pagerank(sub_graph)
        users: dict = {}
        for item in sub_graph.vertices():
            users[v_name[item]] = pr[item]
 
        ordered_users = dict(sorted(users.items(), key=lambda item: item[1], reverse = True))
        print("*** Most relevant users ***")
        self.print_map(ordered_users)
        return list(ordered_users.items())
       

    def get_relevant_repos(self) -> list:
        v_name: VertexPropertyMap = self.graph.get_name()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        v_repo_st: VertexPropertyMap = self.graph.get_repo_st()
        v_repo_forks: VertexPropertyMap = self.graph.get_repo_forks()
        v_repo_date: VertexPropertyMap = self.graph.get_repo_date()
        v_is_user: VertexPropertyMap = self.graph.get_is_user()
        v_no_main: VertexPropertyMap = self.graph.get_no_main()

        #Remove main vertex because is supernode.
        sub_graph = GraphView(self.graph.g, v_no_main)

        personalized_vector = sub_graph.new_vertex_property("double")
        num_vertices = sub_graph.num_vertices()

        # Set 1 to users in personalized PageRank.
        users = v_is_user.a >= 1
        personalized_vector.a[users] = 1/num_vertices

        # Repositories with more than 1000 stargazers
        starg = v_repo_st.a >= 1000  
        personalized_vector.a[starg] = 1/num_vertices

        # Repositories with more than 100 forks
        forks = v_repo_forks.a >= 100 
        personalized_vector.a[forks] = 1/num_vertices

        # Repositories that have been created during the last year.
        yearago = date.today() - timedelta(365)
        for item in sub_graph.iter_vertices():
            year = v_repo_date[item][:4]
            month = v_repo_date[item][5:7]
            day = v_repo_date[item][8:10]
            if year:
                dateobj = date(int(year), int(month), int(day))
                res = yearago - dateobj   
                if res.days < 0: personalized_vector[item] = 1/num_vertices

        # Personalized pagerank
        pr = pagerank(sub_graph, pers=personalized_vector)

        repos: dict = {} 
        for item in self.graph.g.iter_vertices():
            if v_is_repo[item] == 1:
                repos[v_name[item]] = pr[item]
        
        ordered_repos = dict(sorted(repos.items(), key=lambda item: item[1], reverse = True))
        print("*** Most relevant repos ***")
        self.print_map(ordered_repos)
        return list(ordered_repos.items())
           

    def get_topics(self) -> list:
        v_repo_topics: VertexPropertyMap = self.graph.get_repo_topics()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        sub_graph = GraphView(self.graph.g, v_is_repo)

        topics: dict = {}
        for repo  in sub_graph.iter_vertices():
            for topic in v_repo_topics[repo]:
                if topic in topics:
                    topics[topic] += 1
                elif topic != 'None': 
                    topics[topic] = 1

        ordered_topics = dict(sorted(topics.items(), key=lambda item: item[1], reverse = True))    
        print("*** Topics ***")
        self.print_map(ordered_topics)
        return list(ordered_topics.items())
        
    def get_languages(self) -> list:
        v_repo_lang: VertexPropertyMap = self.graph.get_repo_lang()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        sub_graph = GraphView(self.graph.g, v_is_repo)

        languages: dict = {}
        for repo in sub_graph.iter_vertices():
            if v_repo_lang[repo] in languages:
                languages[v_repo_lang[repo]] += 1
            elif v_repo_lang[repo] != 'None': 
                languages[v_repo_lang[repo]] = 1
        
        ordererd_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse = True))
        print("*** Languages ***")
        self.print_map(ordererd_languages)
        return list(ordererd_languages.items())


    def get_licenses(self) -> list:
        v_repo_license = self.graph.get_repo_license()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        sub_graph = GraphView(self.graph.g, v_is_repo)

        licenses: dict = {}
        for repo in sub_graph.iter_vertices():
            if v_repo_license[repo] in licenses:
                licenses[v_repo_license[repo]] += 1
            elif v_repo_license[repo] and  v_repo_license[repo] != "Other": 
                licenses[v_repo_license[repo]] = 1

        ordered_licenses = dict(sorted(licenses.items(), key=lambda item: item[1], reverse = True))    
        print("*** Licenses ***")
        self.print_map(ordered_licenses)
        return list(ordered_licenses.items())

    def print_map(self, topi) -> None:
        for key,value in islice(topi.items(), 0, 10):
            print(key, ':', value)
    

           
    