from curses import resetty
from itertools import islice
from datetime import date, timedelta
from graph_tool.all import *
from models import interestGraph

class dataProcessing:

    def __init__(self) -> None:
        pass

    def get_relevant_users(graph: interestGraph) -> None:
        graph_properties: list = graph.get_graph_properties()
        v_name: VertexPropertyMap = graph_properties[0]
        v_is_user: VertexPropertyMap = graph_properties[1]
        sub_graph = GraphView(graph.g, v_is_user)
        
        pr = pagerank(sub_graph)
        results: list = [(v_name[item], pr[item]) for item in sub_graph.vertices()]
 
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant users ***")
        for item in results[:10]:
                print(item)   
        print("-----------------------------------------")


    def get_relevant_repos(graph: interestGraph) -> None:
        graph_properties: list = graph.get_graph_properties()
        v_name: VertexPropertyMap = graph_properties[0]
        v_is_repo: VertexPropertyMap = graph_properties[2]
        v_repo_st: VertexPropertyMap = graph_properties[3]
        v_repo_forks: VertexPropertyMap = graph_properties[5]
        v_repo_date: VertexPropertyMap = graph_properties[6]

        personalized_vector = graph.g.new_vertex_property("double")

        # Repositories with more than 1000 stargazers
        starg = v_repo_st.a >= 1000  
        personalized_vector.a[starg] += 1

        # Repositories with more than 100 forks
        forks = v_repo_forks.a >= 100 
        personalized_vector.a[forks] += 1

        # Repositories that have been created during the last year.
        yearago = date.today() - timedelta(365)
        for item in graph.g.iter_vertices():
            year = v_repo_date[item][:4]
            month = v_repo_date[item][5:7]
            day = v_repo_date[item][8:10]

            if year:
                dateobj = date(int(year), int(month), int(day))
                res = yearago - dateobj
            
            if res.days > 0: personalized_vector[item] += 1 

        # Personalized pagerank
        pr = pagerank(graph.g, pers=personalized_vector)

        results: list = [] 
        for item in graph.g.iter_vertices():
            if v_is_repo[item] == 1:
                results.append((v_name[item], pr[item]))
        
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant repos ***")
        for item in results[:10]:
                print(item)   
        print("-----------------------------------------")



    def get_languages(graph) -> None:
        graph_properties: list = graph.get_graph_properties()
        v_repo_lang: VertexPropertyMap = graph_properties[4]
        v_is_repo: VertexPropertyMap = graph_properties[2]
        sub_graph = GraphView(graph.g, v_is_repo)

        languages: dict = {}
        for repo  in sub_graph.iter_vertices():
            if v_repo_lang[repo] in languages:
                languages[v_repo_lang[repo]] += 1
            elif v_repo_lang[repo] != 'None': 
                languages[v_repo_lang[repo]] = 1
        
        lang = dict(sorted(languages.items(), key=lambda item: item[1], reverse = True))
        
        print("*** Languages ***")
        for key,value in islice(lang.items(), 0, 10):
	        print(key, ':', value)