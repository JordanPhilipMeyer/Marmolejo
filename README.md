# Marmolejo
I use the calendar app like a task manager in a sense. I give all my tasks a block on time in Google Calendar.  With Marmolejo, users can easily review events over their week in Google calendar and evaluate its status. Track tasks that are incomplete and need to be scheduled with time in the future. In the future, users may be able to predict the likelihood of completing an event based on event description, time of day, and history of completion. 

## Steps to get set up:
- `git clone <url>`

- `pip install -r requirements.txt`

- Get credentials from Google api. See Google's developer documentation on [access credentials](https://developers.google.com/workspace/guides/create-credentials) for their API. OAuth credentials should work for most people with a Google account trying to launch this app locally. 

  ![image-20220119205105000](/home/jordan/.config/Typora/typora-user-images/image-20220119205105000.png)

- Once completed, you should see an action to download a json with your credentials. Rename this file `credentials.json` and store it in your project directory. When you run `main.py` later, you will be prompted to give your app access to your Google account through a browser.

- If there are any events you want your tracker to skip over, write these event names on a new line in the file
  `events_to_ignore.txt`. I find this useful to skip over blocks in my calendar for morning and evening routines.

- In the terminal, run `python init_db.py`

- In the terminal, run `python main.py`

- Walk through using `task_util.py` functions: `read_all_incomplete_tasks`, `grab_random_set_of_tasks_to_update`

## Database structure
In our event database, we have a task journal table. This logs all our unique events. See the data dictionary below:

| Element          | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| eventID          | Google event ID tag. See Google API docs                     |
| eventName        | Name of Google event                                         |
| eventDescription | Content stored in the notes section of a google event        |
| eventDate        | full time stamp of the event                                 |
| eventDay         | day of the week of the event                                 |
| complete         | indicates whether the event was completed on first review (y- yes / n- no / i- ignore ) |
| updated          | indicates whether the event was completed at a later time or ready to be removed from the curator of missed events |

## Target directory structure

```
├── credentials.json
├── eventDB.db
├── events_to_ignore.txt
├── init_db.py
├── logs
│   └── task_journal_2021-12-26.csv
├── main.py
├── README.md
├── requirements.txt
├── task_util.py
├── token.json
└── venv
```


## Troubleshooting
- Reset the credential json once a week. At the time of development, a token usually provides access to the Google API for a week.
    - Reset the credential. Execute main, which should take you to a Google portal to verify identity.

