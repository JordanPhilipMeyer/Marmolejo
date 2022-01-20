import pandas as pd
import sqlite3

## USES THE TASK JOURNAL CSV AS A SIMPLE SCHEMA FOR YOUR DATABASE
df = pd.read_csv("logs/task_journal_2021-12-26.csv")
df.drop(df.index, inplace=True)
try:
    conn = sqlite3.connect("eventDB.db")
    df.to_sql("task_journal", conn, if_exists="replace", index=False)
    conn.close()
except Exception as err:
    print(f"Database write action failed: {str(err)}")