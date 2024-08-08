import sqlite3
import pandas as pd

conn = sqlite3.connect("datasets/loan_small.db")
loans = pd.read_sql_query("SELECT * FROM records", conn)
print(loans.head())
