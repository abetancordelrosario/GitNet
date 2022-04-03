import click
from command import command
from models.draw import draw
from models.interestGraph import interestGraph
from models.algorithms import algorithms  
import time


def command_line() -> None:
    cli = command()
    cli.cli()



def main() -> None:   
    graph = interestGraph("marius92mc/github-stargazers","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")
    # graph = interestGraph("azat-co/react","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")
    initialTime = time.time()
    
    graph.create_graph()
    
    algorithms.get_relevant_users(graph)
    algorithms.get_relevant_repos(graph)
    algorithms.get_languages(graph)
    # draw.draw_graph(graph)

    print("Tiempo que tarda en ejecutar el programa:", (time.time() - initialTime), "seconds")
    print(graph.g.num_vertices)

if __name__ == "__main__":
    main()
    # command_line()
