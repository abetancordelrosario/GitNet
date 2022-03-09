from matplotlib import testing
from models.createGraph import createGraph
from tests.test_createGraph import test_createGraph

def main() -> None:   
    graph = createGraph()
    graph.add_nodes_and_edges()

def execute_tests():
    testing = test_createGraph()
    testing.test()

if __name__ == "__main__":
    #main()
    execute_tests()