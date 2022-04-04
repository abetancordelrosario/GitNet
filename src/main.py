from command import command
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing  
import time


def command_line() -> None:
    cli = command()
    cli.cli()



def main() -> None:   

    initialTime = time.time()

    graph = interestGraph("marius92mc/github-stargazers","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")
    
    graph.create_graph()
    
    dataProcessing.get_relevant_users(graph)
    dataProcessing.get_relevant_repos(graph)
    dataProcessing.get_languages(graph)
    # draw.draw_graph(graph)

    print("Tiempo que tarda en ejecutar el programa:", (time.time() - initialTime), "seconds")
    print(graph.g.num_vertices)

if __name__ == "__main__":
    main()
    # command_line()
