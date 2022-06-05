import argparse
from prompt_toolkit import PromptSession
from models.XGBoost.xgbDataProcessing import xgbDataProcessing

from models.dataExtraction import dataExtraction
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing
from models.dataVisualization import dataVisualization
from models.manageGraph import manageGraph

class Command:

    __OPTIONS = {'users': 'get_relevant_users', 'repos': 'get_relevant_repos', 'languages': 'get_languages', 
                'licenses': 'get_licenses', 'topics': 'get_topics', 'draw': 'draw', "help": 'show_help',
                'repos_xgb': 'get_relevant_repos_xgb'}

    __FORMATS: list = ['gt', 'graphml', 'xml', 'dot',  'gml']

    def start_cli(self) -> None:
        parser = argparse.ArgumentParser(description="GitNet")
        group = parser.add_argument_group('group')
        group.add_argument("-r", "--repository", help="Enter full name of the repository (author/repo)")
        group.add_argument("-t", "--token", help="Enter OAuth GitHub token")
        parser.add_argument("-l", "--load", help="Enter the name of a graph file")
        args = parser.parse_args()
        self.process_arguments(args.repository, args.token, args.load)

    def repl(self) -> None:
        session = PromptSession()
        while True:
            try:
                text = session.prompt('> ')
                if text in self.__OPTIONS:
                    method = getattr(self, self.__OPTIONS[text])
                    method()
                    print("-----------------------------------------")
                elif text.split(" ")[0] == 'save' and len(text.split()) == 2:
                    self.save_graph(text)
                else:
                    print("""Invalid argument. Write 'help' to see valid arguments.""")
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        print(self.graph.g.num_vertices)
        print('GoodBye!')
    
    def process_arguments(self, repository: str, token: str, load: str):
        if load is None:
            extract = dataExtraction(repository,token)
            self.graph = interestGraph(extract)
            self.graph.create_graph()
            self.dp = dataProcessing(self.graph)
            self.dv = dataVisualization()
            self.repl()
        else:
            g = manageGraph.load(load)
            self.graph = interestGraph(g)
            self.dp = dataProcessing(self.graph)
            self.dv = dataVisualization()
            self.repl()

    def get_relevant_users(self) -> None:
        result_data = self.dp.get_relevant_users()
        self.dv.plot_barChart(result_data, "Most relevant users")
        self.dv.plot_pieChart(result_data)
    
    def get_relevant_repos(self) -> None:
        result_data = self.dp.get_relevant_repos()
        self.dv.plot_pieChart(result_data)
        self.dv.fork_relationship(result_data, self.graph)
    
    def get_languages(self) -> None:
        result_data = self.dp.get_languages()
        self.dv.plot_barChart(result_data, "Popular programming languages")
        self.dv.plot_pieChart(result_data)
        
    def get_topics(self) -> None:
        result_data = self.dp.get_topics()
        self.dv.plot_barChart(result_data, "Popular topics")
        self.dv.plot_pieChart(result_data)
    
    def get_licenses(self) -> None:
        result_data = self.dp.get_licenses()
        self.dv.plot_barChart(result_data, "Popular licenses")
        self.dv.plot_pieChart(result_data)

    def get_relevant_repos_xgb(self) -> None:
        xgbdata = xgbDataProcessing()
        xgbdataframe, names_column = xgbdata.create_dataframe(self.graph)
        self.dp.xgboost_repos(xgbdataframe, names_column)
        
    def draw(self):
        draw.draw_graph(self.graph)

    def save_graph(self, file_format) -> None:
        if file_format.split(" ")[1] in self.__FORMATS:
            manageGraph.save_graph(self.graph, file_format.split(" ")[1])
            print("Graph have been saved correctly in /data folder")
        else:
            print("Invalid format. Write 'help' to see valid arguments.")

    def show_help(self) -> None:
        print("""
        user        --> Get most important users with PageRak algorithm.
        
        repo        --> Get most important repositories with personalized PageRank algorithm. 
                        The personalization vector benefit repos with more than 1000 stargazers,
                        more than 100 forks and those that have been created in the last year.
                
        languages   --> Get the programming language of other repositories that the stargazers
                        stars.

        topics      --> Get the programming topics of other repositories that the stargazers
                        stars. 

        licenses    --> Get the licenses of other repositories that the stargazers
                        stars.
        
        draw        --> Draw graph and save it in PDF format.

        save        --> Save the graph. The second parameter is the format of the file, gt (recommended), 
                        graphml, xml , dot ,  gml. 
        
        """)