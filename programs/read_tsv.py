import pandas as pd
from create_db import create_database


create_db1 =create_database("database.db")

df =pd.read_csv('questions2.tsv', sep='\t')


Category = list(df['Category'])
Question = list(df['Question'])
choices_a = list(df['a'])
choices_b = list(df['b'])
choices_c = list(df['c'])
choices_d = list(df['d'])
correctanswer = list(df['correctanswer'])
pathOfImage = list(df['pathOfImage'])

for a in range(len(Category)):
    create_db1.insertQuestion(Category[a],Question[a],choices_a[a],choices_b[a],choices_c[a],choices_d[a],correctanswer[a],pathOfImage[a])