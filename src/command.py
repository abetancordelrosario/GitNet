import argparse
from prompt_toolkit import PromptSession

from models.dataExtraction import dataExtraction
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing
from models.dataVisualization import dataVisualization as dv

class Command:

    __OPTIONS = {'users': 'get_relevant_users', 'repos': 'get_relevant_repos', 'languages': 'get_languages', 
                'licenses': 'get_licenses', 'topics': 'get_topics', 'draw': 'draw', "help": 'show_help'}

    def start_cli(self) -> None:
        parser = argparse.ArgumentParser(description="GitNet")
        parser.add_argument("-r", "--repository", required=True, help="Enter full name of the repository (author/repo)")
        parser.add_argument("-t", "--token", required=True, help="Enter OAuth GitHub token")
        args = parser.parse_args()
        self.repl(args.repository, args.token)


    def repl(self, repository, token) -> None:
        session = PromptSession()
        extract = dataExtraction(repository,token)
        self.graph = interestGraph(extract)
        self.graph.create_graph()
        self.dp = dataProcessing(self.graph)
        while True:
            try:
                text = session.prompt('> ')
                if text in self.__OPTIONS:
                    method = getattr(self, self.__OPTIONS[text])
                    method()
                    print("-----------------------------------------")
                else:
                    print("""Invalid argument. Write 'help' to see valid arguments.""")
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        print(self.graph.g.num_vertices)
        print('GoodBye!')

    def get_relevant_users(self):
        result_data = self.dp.get_relevant_users()
        dv.plot_barChart(result_data, "Most relevant users")
        dv.plot_pieChart(result_data, "Most relevant users")
    
    def get_relevant_repos(self):
        result_data = self.dp.get_relevant_repos()
        dv.plot_pieChart(result_data, "Most relevant repositories")
    
    def get_languages(self):
        result_data = self.dp.get_languages()
        dv.plot_barChart(result_data, "Popular programming languages")
        dv.plot_pieChart(result_data, "Most relevant languages")
        
    def get_topics(self):
        result_data = self.dp.get_topics()
        dv.plot_barChart(result_data, "Popular topics")
        dv.plot_pieChart(result_data, "Popular topics")
    
    def get_licenses(self):
        result_data = self.dp.get_licenses()
        dv.plot_barChart(result_data, "Popular licenses")
        dv.plot_pieChart(result_data, "Popular licenses")
        
    def draw(self):
        draw.draw_graph(self.graph)
            
    def show_help(self):
        print("""
        user        --> Get most important users with PageRak algorithm.
        
        repo        --> Get most important repositories with personalized PageRank algorithm. 
                        The personalization vector benefit repos with more than 1000 stargazers,
                        more than 100 forks and those that have been created in the last year.
                
        languages   --> Get the programming language of other repositories that the stargazers
                    stars.

        topics      --> Get the programming topics of other repositories that the stargazers
                        stars. 

        licenses    --> Get the licenses language of other repositories that the stargazers
                        stars.
        
        draw        --> Draw graph and save it in PDF format.
        
        """)