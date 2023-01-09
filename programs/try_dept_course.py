import pandas as pd
from create_db import create_database
import joblib

def sort_index(lst, rev=True):
    index = range(len(lst))
    s = sorted(index, reverse=rev, key=lambda i: lst[i])
    return s

create_db1 =create_database("database.db")

dc =pd.read_csv('Department_Courses.tsv', sep='\t')

print(list(dc["COLLEGE OF ARTS AND SCIENCES"]))

model = joblib.load("regression.pkl")

Y_pred_rf_proba = list(model.predict_proba([[80,50,80,70,90,90]])[0])
Y_pred_rf_proba = sort_index(Y_pred_rf_proba)

print(Y_pred_rf_proba[:3])

    