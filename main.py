from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

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
    creds = None
    format_save = []
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
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day

        # now = datetime.datetime(2021,12,26).isoformat() + 'Z'
        maxtime = datetime.datetime(year,month,day).isoformat() + 'Z'
        week_back = (datetime.datetime(year,month,day) - datetime.timedelta(days=8)).isoformat() + 'Z'
        format_save.append(week_back)

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
            # print(start, event['summary'])

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
            event_log.append(rec)


    except HttpError as error:
        print('An error occurred: %s' % error)

    # format_save = str(year) + str(month) + str(day)
    df = pd.DataFrame(event_log, columns=["eventID", "eventName", "eventDescription", "eventDate", "eventDay", "complete"])
    df.to_csv(f"logs/my_test_{format_save[0][:10]}.csv")

if __name__ == '__main__':
    main()

    #Generate a list of tasks that have been incomplete over the last N weeks

    #Write a function to update the calendar event to write to my calendar a new date

    #schedule runs on linux

    #future ideas in readme: model to predict whether an event will be completed
