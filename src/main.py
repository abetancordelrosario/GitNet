from command import Command
from models.dataExtraction import dataExtraction
from models.draw import draw
from models.interestGraph import interestGraph
from models.dataProcessing import dataProcessing  
import time



def main() -> None:
    cli = Command()
    cli.start_cli()

if __name__ == "__main__":
    main()
    
