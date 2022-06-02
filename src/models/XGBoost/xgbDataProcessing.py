import pandas as pd
from datetime import date, timedelta

from ..interestGraph import interestGraph 
from ..dataProcessing import dataProcessing 

class xgbDataProcessing:
    
    def create_dataframe(self, graph: interestGraph) -> None:
        main_repo: str =  graph.get_repo_name()
        stargazers_starred: list = graph.get_stargazers_starred_repos()
        starred_repos: list = [repo for stargazer in stargazers_starred for repo in stargazer]
        
        dp = dataProcessing(graph)
        relevant_repos: list = dp.get_relevant_repos()
        relevant_repos = relevant_repos[:50]
        labels: list = [] 
        sizes: list = []
        for key, value in relevant_repos:
            labels.append(key)
        print(labels)

        df = pd.DataFrame.from_records(starred_repos)
        df.drop(labels=df.columns.difference(['full_name',
                                        'created_at',
                                        'stargazers_count',
                                        'forks_count',
                                        'open_issues_count']),
                                         axis=1,
                                         inplace=True)
        df['count'] = df.groupby('full_name')['full_name'].transform('count')
        df = df.drop_duplicates()
        self.set_created_at_value(df)
        self.set_relevant_repos(df, relevant_repos)
    
        df.to_csv(f"data/{main_repo}")
        # print(df)

    def set_created_at_value(self, df: pd.DataFrame) -> pd.DataFrame:
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
        
        return df

    
    def set_relevant_repos(self, df: pd.DataFrame, relevant_repos: list) -> pd.DataFrame:
        df['is_relevant'] = ""
        for repo in relevant_repos:
            if repo in df['full_name']:
                print("está")