# gcal_weekly_reviewer
I use the calendar app like a task manager in a sense. I give all things a 
block of time to complete the task. The goal of this app is to easily review my 
week and evaluate what's complete and what might need to be revisited in the future.

## Steps to get set up:
- `git clone <url>`
- `pip install -r requirements.txt`
- Get credentials from Google api. Include links and documentation. 
You should have a credentials.json file that will be stored in the project directory
`google event script`
You will be prompted to give your app acces to your Google account. 
- In the project root, add a text file called `events_to_ignore.txt`. On a new line, add the name of any google events 
that you want to skip over. 
- launch `main.py`

- Walkthrough using task_util functions: `read_all_incomplete_tasks`, `grab_random_set_of_tasks_to_update`

## Database structure
Create a sqlite database to store events. I'll name mine `eventDB.db`
In the root of the project run: `sqlite3 eventDB.db`
In the sqlite shell run: `.databases`. Should return something like: 
`~/google event script/eventDB.db`

Use a task journal template to structure the database. In an ipython terminal:
```
import pandas as pd
import sqlite3
df = pd.read_csv("logs/task_journal_2021-12-26.csv")
conn = sqlite3.connect("eventDB.db")
df.to_sql("task_journal", conn, if_exists="replace", index=False)
```

Event Id, Event Name, Event Description, Time scraped, complete?, Revision

## Target directory structure
```
├── credentials.json
├── events_to_ignore.txt
├── incomplete
│   └── incomplete_tasks_2022-01-12.md
├── logs
│   ├── scraped_logs_list.txt
│   ├── task_journal_2021-12-26.csv
│   ├── task_journal_2021-12-28.csv
│   └── task_journal_2022-01-04.csv
├── main.py
├── README.md
├── requirements.txt
├── task_util.py
├── token.json
└── venv
```


## Troubleshooting
- May need to delete the file `incomplete_tasks_{date}.md` and `scraped_logs_list.txt` if errors crop up
- Reset the credential json once a week.
    - Reset the credential. Execute main, which should take you to a Google portal to verify identity.


