# gcal_weekly_reviewer
I use the calendar app like a task manager in a sense. I give all things a 
block of time to complete the task. The goal of this app is to easily review my 
week and evaluate what's complete and what might need to be revisited in the future.

## Steps to get set up:
- Create a directory called `logs` This will be the save location for our weekly review.
- Get credentials from Google api. Include links and documetnation. 
You should have a credentials.json file that will be stored in the project directory
`google event script`
- Pip install from requirements
- launch `main.py`

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


