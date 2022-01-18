import pandas as pd
# from os import listdir
# from os.path import isfile, join
# from datetime import datetime
# from pathlib import Path
import sqlite3

# def launch_incomplete_task_compiler():
#     """DEPRECIATE FOR SQLITE QUERY"""
#     date_now = str(datetime.now())[:10]
#     file_with_incompletes = f"incomplete/incomplete_tasks_{date_now}.md" # file that will hold incomplete tasks to revisit
#     file_with_scrap_list = 'logs/scraped_logs_list.txt'
#
#     prior_files_scraped = [] # list of files that have already been processed so that tasks are not duplicated on markdown
#     with open('logs/scraped_logs_list.txt') as f:
#         prior_files_scraped.extend(f.read().splitlines())
#     print(prior_files_scraped)
#
#     onlyfiles = [f for f in listdir("logs") if isfile(join("logs", f)) & (f[-3:] == "csv")] #get all csv files in logs
#     full_undone = pd.DataFrame(columns=["eventName", "eventDescription"])
#     # files_to_add_to_scrap_list = []
#     for file in onlyfiles:
#         if file in prior_files_scraped:
#             print(f"already passed {file} for task list clean up")
#             continue
#         else:
#             df = pd.read_csv("logs/" + file)
#             undone = df[df.complete=="n"]
#             print(undone[["eventName", "eventDescription"]])
#             full_undone = pd.concat([full_undone[["eventName", "eventDescription"]],
#                                      undone[["eventName", "eventDescription"]]]).reset_index()
#             with open(file_with_scrap_list, 'a') as f:
#                 f.write(f'\n{file}')
#
#     if Path(file_with_incompletes).is_file():
#         print("FILE EXISTS. NO SAVE OCCURED.")
#     else:
#         full_undone[["eventName", "eventDescription"]].to_markdown(file_with_incompletes, index=False, tablefmt="simple")

def read_all_incomplete_tasks(ignore_updates=True):
    conn = sqlite3.connect("eventDB.db")
    if ignore_updates:
        df = pd.read_sql("SELECT * FROM task_journal WHERE complete = 'n';", conn)
    else:
        df = pd.read_sql("SELECT * FROM task_journal WHERE complete = 'n' AND updated IS NULL;", conn)
    conn.close()
    return df

def grab_random_set_of_tasks_to_update(n_to_sample):
    conn = sqlite3.connect("eventDB.db")

    incomplete_sample = read_all_incomplete_tasks().sample(n_to_sample).copy()
    for event in incomplete_sample.eventID.unique():
        print(incomplete_sample[incomplete_sample.eventID==event].to_markdown())
        x = int(input("Should this task be removed from running incomplete set? Answer 1 or 0. 1 = Remove."))
        if x==1:
            sql_ = f"UPDATE task_journal SET updated = 'y' WHERE eventID = '{event}'"
            conn.execute(sql_)
            conn.commit()
    conn.close()


# TODO predict likihood that task is completed in future