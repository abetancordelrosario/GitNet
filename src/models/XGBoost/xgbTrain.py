import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve
from sklearn.metrics import average_precision_score
import xgboost

class xgbTrain:
    '''
    Create the machine learning model using cross-validation
    to get the best hyperparametres.
    '''

    def cross_validation(self, df: pd.DataFrame) -> None:
        df = pd.read_csv("data/AliceVision")
        names = df.pop("open_issues_count")
        un_named = df.pop("Unnamed: 0")
 

        relevant_df = df[df['is_relevant'] == 1]
        no_relevant_df = df[df['is_relevant'] == 0]
        print(no_relevant_df.shape[0])  
        print(relevant_df.shape[0])

        X = df.loc[:, df.columns!='is_relevant']
        y = df.loc[:, 'is_relevant']

        X_train, X_test, y_train, y_test= train_test_split(X, y, test_size= 0.5, random_state=1)

        X_valid, X_test, y_valid, y_test= train_test_split(X_test, y_test, test_size= 0.5, random_state=1)

        xgb = xgboost.XGBClassifier()

        parametres = {  'objective': ['binary:logistic'],
                        'learning_rate': [0.25],
                        'n_estimators': [100],
                        'reg_alpha': [1],
                        'gamma': [0],
                        'early_stopping_rounds': [20],
                        'eval_metric': ['aucpr'],
                        'max_depth': [5]
                        }

        fit_params = { 'eval_set': [(X_test, y_test)]}

        clf =  GridSearchCV(xgb, parametres, cv=5, scoring='average_precision')
        clf.fit(X_train, y_train, **fit_params)


        print(clf.best_estimator_)
        print(clf.best_params_)
        print("Testing")
        print(clf.best_score_)

        best_xgb = clf.best_estimator_
        y_preds = best_xgb.predict(X_valid)

        comp = pd.DataFrame({'real': y_valid, 'preds': y_preds})
        comp.to_csv(f"data/validation")

        acc = average_precision_score(y_valid, y_preds)
        print("Validación")
        print(acc)


    def create_model(self, df: pd.DataFrame) -> None:
        df = pd.read_csv("data/AliceVision")
        names = df.pop("open_issues_count")
        un_named = df.pop("Unnamed: 0")
 

        relevant_df = df[df['is_relevant'] == 1]
        no_relevant_df = df[df['is_relevant'] == 0]
        print(no_relevant_df.shape[0])  
        print(relevant_df.shape[0])

        X = df.loc[:, df.columns!='is_relevant']
        y = df.loc[:, 'is_relevant']

        X_train, X_test, y_train, y_test= train_test_split(X, y, test_size= 0.5, random_state=1)

        X_valid, X_test, y_valid, y_test= train_test_split(X_test, y_test, test_size= 0.5, random_state=1)

        xgb = xgboost.XGBClassifier(objective= 'binary:logistic',
                                    learning_rate=0.25,
                                    n_estimators=100,
                                    gamma=0,
                                    eval_metric='aucpr',
                                    max_depth=5
                                    )


        # best_xgb.save_model("xgb_model/model.json)"
        xgb.fit(X_train, y_train)

        xgb.save_model("xgb_model/model.json")

        model = xgboost.XGBClassifier()
        model.load_model("xgb_model/model.json")

        print(X_valid)
        y = model.predict(X_valid)
        print(y.tolist())
        

   

    

        



