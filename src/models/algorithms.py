from itertools import islice
import string
from graph_tool.all import *
from models import interestGraph

class algorithms:

    def __init__(self):
        pass

    def get_relevant_users(graph: interestGraph):
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


    def get_relevant_repos(graph: interestGraph):
        graph_properties: list = graph.get_graph_properties()
        v_name: VertexPropertyMap = graph_properties[0]
        v_is_repo: VertexPropertyMap = graph_properties[2]
        v_repo_st: VertexPropertyMap = graph_properties[3]

        # print(v_repo_st.a)
        # print("--------------------------------------")
        pr_prop = v_repo_st.a >= 1000
        pr_prop_2 = v_repo_st.a < 1000
        p = graph.g.new_vertex_property("double")
        p.a[pr_prop] = 2
        p.a[pr_prop_2] = 1
        # print(p.a)

        pr = pagerank(graph.g, pers=p)
        results: list = [] 
        for item in graph.g.vertices():
            if v_is_repo[item] == 1:
                results.append((v_name[item], pr[item]))
        
        results.sort(key = lambda element: element[1], reverse = True)
        print("*** Most relevant repos ***")
        for item in results[:10]:
                print(item)   
        print("-----------------------------------------")



    def get_languages(graph):
        graph_properties: list = graph.get_graph_properties()
        v_repo_lang: VertexPropertyMap = graph_properties[4]
        v_is_repo: VertexPropertyMap = graph_properties[2]
        sub_graph = GraphView(graph.g, v_is_repo)

        print("*** Languages ***")

        languages: dict = {}
        for repo  in sub_graph.iter_vertices():
            if v_repo_lang[repo] in languages:
                languages[v_repo_lang[repo]] += 1
            elif v_repo_lang[repo] != 'None': 
                languages[v_repo_lang[repo]] = 1
        
        lang = dict(sorted(languages.items(), key=lambda item: item[1], reverse = True))
        for key,value in islice(lang.items(), 0, 10):
	        print(key, ':', value)