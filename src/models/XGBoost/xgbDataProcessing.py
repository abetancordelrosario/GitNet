from typing import Tuple
import pandas as pd
from datetime import date, timedelta

from models.XGBoost.xgbTrain import xgbTrain
from ..interestGraph import interestGraph 
from ..dataProcessing import dataProcessing 

class xgbDataProcessing:
    '''
    Generate dataframe with the data fetched from the GitHub
    API, then clean the data for creating the training dataset,
    or for creating the dataset for the prediction.
    '''
    
    def create_dataframe(self, graph: interestGraph) -> Tuple:
        stargazers_starred: list = graph.get_stargazers_starred_repos()
        starred_repos: list = [repo for stargazer in stargazers_starred for repo in stargazer]

        df = pd.DataFrame.from_records(starred_repos)
        df.drop(labels=df.columns.difference(['full_name',
                                        'created_at',
                                        'stargazers_count',
                                        'forks_count'
                                        ]),
                                         axis=1,
                                         inplace=True)
        df['count'] = df.groupby('full_name')['full_name'].transform('count')
        df = df.drop_duplicates()
        self.set_created_at_value(df)

        # self.create_training_dataset(graph, df)
        
        names = df.pop("full_name")
        df.to_csv(f"data/temp")

        return df, names


    def set_created_at_value(self, df: pd.DataFrame) -> None:
        yearago = date.today() - timedelta(365)

        for index, row in df.iterrows():
            year = row['created_at'][:4]
            month = row['created_at'][5:7]
            day = row['created_at'][8:10]
            if year:
                dateobj = date(int(year), int(month), int(day))
                res = yearago - dateobj   
                if res.days < 0: 
                    df.loc[index, 'created_at'] = 1
                else:
                    df.loc[index, 'created_at'] = 0
        
 
    def set_relevant_repos(self, df: pd.DataFrame, repo_names: list) -> None:
        df['is_relevant'] = ""
        df['is_relevant'].values[:] = 0
        repos_index = []
        for repo in repo_names:
            if repo in df.full_name.values:
                index = df.index[df['full_name'] == repo].tolist()
                df.loc[index, 'is_relevant'] = 1
                repos_index.append(index)
        
    def create_training_dataset(self, graph: interestGraph, df: pd.DataFrame) -> None:
        main_repo: str =  graph.get_repo_name()

        dp = dataProcessing(graph)
        relevant_repos: list = dp.get_relevant_repos()
        repos_number = len(relevant_repos)
        number = repos_number/10
        number = int(number)
        relevant_repos = relevant_repos[:number]
        repo_names: list = [] 
        for key, _ in relevant_repos:
            repo_names.append(key)

        self.set_relevant_repos(df, repo_names)
        relevant_df = df[df['is_relevant'] == 1]
        no_relevant_df = df[df['is_relevant'] == 0]
        number_no_relevant = no_relevant_df.shape[0] - relevant_df.shape[0]
        remove_df = no_relevant_df.sample(n = number_no_relevant)
        remove_df_list = remove_df.index.values.tolist() 

        for index in remove_df_list:
            df.drop(index, inplace=True)
        
        df.to_csv(f"data/{main_repo}")
        names = df.pop("full_name")
        xgb = xgbTrain()
        xgb.cross_validation(df)
        df.to_csv(f"data/temp")

        return df, names

    