from command import Command
from models.dataExtraction import dataExtraction
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing  
import time



def cli() -> None:
    c = Command()
    c.start_cli()

def main() -> None:   

    initialTime = time.time()

    # extract = dataExtraction("marius92mc/github-stargazers","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")
    extract = dataExtraction("ternaus/TernausNet","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")
    # extract = dataExtraction("Ventto/mons","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")
    # extract = dataExtraction("azat-co/react","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")
    # extract = dataExtraction("azat-co/react-quickly","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")
    # extract = dataExtraction("yavallejo/tallerwordpress","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")
    graph = interestGraph(extract)
    graph.create_graph()

    # dp = dataProcessing(graph)    
    # dp.get_relevant_users()
    # dp.get_relevant_repos()
    # dp.get_languages()
    # dp.get_topics()
    # dp.get_licenses()
    # draw.draw_graph(graph)

    print("Tiempo que tarda en ejecutar el programa:", (time.time() - initialTime), "seconds")
    print(graph.g.num_vertices)

if __name__ == "__main__":
    main()
    # cli()
