from command import Command
from models.XGBoost.xgbTrain import xgbTrain

def train():
    
    xgb = xgbTrain()
    xgb.train_model(None)

def main() -> None:
    cli = Command()
    cli.start_cli()

if __name__ == "__main__":
    main()
    # train()
    
