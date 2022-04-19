from itertools import islice
from datetime import date, timedelta
from graph_tool.all import *
from models import interestGraph

class dataProcessing:

    def __init__(self, graph: interestGraph) -> None:
        self.graph = graph

    def get_relevant_users(self) -> None:
        v_name: VertexPropertyMap = self.graph.get_name()
        v_is_user: VertexPropertyMap = self.graph.get_is_user()
        sub_graph = GraphView(self.graph.g, v_is_user)
        
        pr = pagerank(sub_graph)
        results: list = [(v_name[item], pr[item]) for item in sub_graph.vertices()]
 
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant users ***")
        for item in results[:10]:
                print(item[0])   
        print("-----------------------------------------")


    def get_relevant_repos(self) -> None:
        v_name: VertexPropertyMap = self.graph.get_name()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        v_repo_st: VertexPropertyMap = self.graph.get_repo_st()
        v_repo_forks: VertexPropertyMap = self.graph.get_repo_forks()
        v_repo_date: VertexPropertyMap = self.graph.get_repo_date()

        personalized_vector = self.graph.g.new_vertex_property("double")

        # Repositories with more than 1000 stargazers
        starg = v_repo_st.a >= 1000  
        personalized_vector.a[starg] += 1

        # Repositories with more than 100 forks
        forks = v_repo_forks.a >= 100 
        personalized_vector.a[forks] += 1

        # Repositories that have been created during the last year.
        yearago = date.today() - timedelta(365)
        for item in self.graph.g.iter_vertices():
            year = v_repo_date[item][:4]
            month = v_repo_date[item][5:7]
            day = v_repo_date[item][8:10]
            if year:
                dateobj = date(int(year), int(month), int(day))
                res = yearago - dateobj   
            if res.days > 0: personalized_vector[item] += 1 

        # Personalized pagerank
        pr = pagerank(self.graph.g, pers=personalized_vector)

        results: list = [] 
        for item in self.graph.g.iter_vertices():
            if v_is_repo[item] == 1:
                results.append((v_name[item], pr[item]))
        
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant repos ***")
        for item in results[:10]:
                print(item[0])   

    def get_topics(self) -> None:
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

        topi = dict(sorted(topics.items(), key=lambda item: item[1], reverse = True))    
        print("*** Topics ***")
        self.print_map(topi)
        
        
    def get_languages(self) -> None:
        v_repo_lang: VertexPropertyMap = self.graph.get_repo_lang()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        sub_graph = GraphView(self.graph.g, v_is_repo)

        languages: dict = {}
        for repo in sub_graph.iter_vertices():
            if v_repo_lang[repo] in languages:
                languages[v_repo_lang[repo]] += 1
            elif v_repo_lang[repo] != 'None': 
                languages[v_repo_lang[repo]] = 1
        
        lang = dict(sorted(languages.items(), key=lambda item: item[1], reverse = True))    
        print("*** Languages ***")
        self.print_map(lang)

    def get_licenses(self) -> None:
        v_repo_license = self.graph.get_repo_license()
        v_is_repo: VertexPropertyMap = self.graph.get_is_repo()
        sub_graph = GraphView(self.graph.g, v_is_repo)

        licenses: dict = {}
        for repo in sub_graph.iter_vertices():
            if v_repo_license[repo] in licenses:
                licenses[v_repo_license[repo]] += 1
            elif v_repo_license[repo] and  v_repo_license[repo] != "Other": 
                licenses[v_repo_license[repo]] = 1

        lis = dict(sorted(licenses.items(), key=lambda item: item[1], reverse = True))    
        print("*** Licenses ***")
        self.print_map(lis)

    def print_map(self, topi):
        for key,value in islice(topi.items(), 0, 10):
            print(key, ':', value)


           
    