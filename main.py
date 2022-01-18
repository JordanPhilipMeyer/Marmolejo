from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from pathlib import Path
import task_util #utility module that filters for incomplete tasks and appends them to a running list for later review
import sqlite3

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

days_of_week = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday"
}

def get_ignore_events():
    with open("events_to_ignore.txt", "r") as fp:
        my_list = []
        for item in fp:
            my_list.append(item.strip())
    return my_list

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    format_save = []
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    maxtime = datetime.datetime(year, month, day).isoformat() + 'Z'
    week_back = (datetime.datetime(year, month, day) - datetime.timedelta(days=8)).isoformat() + 'Z'
    format_save.append(week_back)

    if not Path(f"logs/task_journal_{format_save[0][:10]}.csv").is_file(): #if weekly journal does not exist, create it.
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)

            print('Getting a week of activity')
            events_result = service.events().list(calendarId='primary', timeMin=week_back, timeMax = maxtime,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            to_ignore = get_ignore_events()
            event_log = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                # function to ignore the regular blocked activities
                if event["summary"] in to_ignore:
                    continue
                gid = event["id"]
                start_time = datetime.datetime.fromisoformat(start)
                try:
                    d = event["description"]
                except:
                    d = None

                rec = [gid, event["summary"], d, start_time, days_of_week[start_time.weekday()]]
                print(rec)
                status = None
                while status is None:
                    input_value = input('Did you complete this task? {y/n/i}')
                    try:
                        if input_value in ["y", "n", "i"]:
                            status = input_value
                    except ValueError:
                        print('Not an acceptable value. Try y, n, or i.')
                rec.append(status)
                rec.append(None) # will represent a modifier feature
                event_log.append(rec)

        except HttpError as error:
            print('An error occurred: %s' % error)

        # format_save = str(year) + str(month) + str(day)
        df = pd.DataFrame(event_log, columns=["eventID", "eventName", "eventDescription", "eventDate", "eventDay",
                                              "complete", "updated"])
        conn = sqlite3.connect("eventDB.db")
        df_stored_in_sql = pd.read_sql("SELECT * FROM task_journal", conn)
        df = pd.concat([df,df_stored_in_sql], axis=0).reset_index()
        df = df.drop_duplicates(subset="eventID")

        df.to_sql("task_journal", conn, if_exists="replace", index=False)
    else:
        print(f"task journal already exists for {format_save[0][:10]}")


if __name__ == '__main__':
    main() # updates event DB with prior week's google events

    #schedule runs on linux

    #future ideas in readme: model to predict whether an event will be completed
