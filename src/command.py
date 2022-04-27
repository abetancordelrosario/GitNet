import click
import argparse
from prompt_toolkit import PromptSession, validation

from models.dataExtraction import dataExtraction
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing

class Command:

    # __OPTIONS = {'user': }

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
                if text == "user":
                    self.dp.get_relevant_users()
                elif text == "repos":
                    self.dp.get_relevant_repos()
                elif text == "licenses":
                    self.dp.get_licenses()
                elif text == "lang":
                    self.dp.get_languages()
                elif text == "topics":
                    self.dp.get_topics()
                elif text == "draw":
                    draw.draw_graph(self.graph)
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
    