import argparse
from prompt_toolkit import PromptSession

from models.dataExtraction import dataExtraction
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing

class Command:

    __OPTIONS = {'user': 'get_relevant_users', 'repo': 'get_relevant_repos', 'lang': 'get_languages', 'licen': 'get_licenses',
                'topics': 'get_topics', 'draw': 'draw', "help": 'show_help'}

    def start_cli(self):
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
                else:
                    print("""Bad argument. Write 'help' to see valid arguments.""")
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        print(self.graph.g.num_vertices)
        print('GoodBye!')

    def get_relevant_users(self):
        self.dp.get_relevant_users()
    
    def get_relevant_repos(self):
        self.dp.get_relevant_repos()
    
    def get_languages(self):
        self.dp.get_relevant_repos()
        
    def get_topics(self):
        self.dp.get_relevant_repos()
    
    def get_licenses(self):
        self.dp.get_relevant_repos()
        
    def draw(self):
        draw.draw_graph(self.graph)
            
    def show_help(self):
        print("""
        user   --> Get most important users with PageRak algorithm.
        
        repo   --> Get most important repositories with personalized PageRank algorithm. 
                   The personalization vector benefir repos with more than 1000 stargazers,
                   more than 100 forks and those that have been created in the last year.
                
        lang   --> Get the programming language of other repositories that the stargazers
                    stars.

        topics --> Get the programming topics of other repositories that the stargazers
                   stars. 

        licen  --> Get the licenses language of other repositories that the stargazers
                    stars.
        
        """)