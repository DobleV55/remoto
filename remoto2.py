from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from calendar import Calendar
from collections import defaultdict
import datetime
import pickle
import os.path
import pprint
import random
import time


current_month_days = [day for day in Calendar().itermonthdates(year, month) if day.weekday() not in [5,6] and day.month == month]

dev =['leo', 'mati', 'diego', 'eric', 'mariano', 'jorge', 'mateo',]

adm = ['yo', 'nadia', 'josh', 'monica', 'mauricio', 'timoteo', 'bauti']

sales = ['Dominica', 'pedro', 'gonza', 'tarta', 'alan', 'julian']

consultoria = ['eze', 'lisandro', 'roberto', 'rodrigo', 'josefina', 'lisa']

GROUPS = [dev, adm, sales, consultoria]

valid_days = current_month_days[:12]
valid_days_2 = current_month_days[13:]

def choose_remoto_days(groups):
    res = {}
    usados = defaultdict(int)
    for members in groups:
      for member in members:      
            remoto_1 = (random.choice(valid_days))
            usados[remoto_1] += 1
            if usados[remoto_1] == 3:
                valid_days.remove(remoto_1)           
            remoto_2 = (random.choice(valid_days_2))
            usados[remoto_2] += 1          
            if usados[remoto_2] == 3:
                valid_days_2.remove(remoto_2) 
            res[member]=[remoto_1, remoto_2]
    return res

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_events(events):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'storage.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    for member, dates in events.items():
        for date in dates:
            event_data = create_event_data(member, date)
            event = service.events().insert(calendarId='primary', body=event_data).execute()
            time.sleep(0.5)
            print ('Event created: %s' % (event.get('htmlLink')))
    
def create_event_data(member, date):
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
        
    event = {
             'summary': member,
              'start': {
                'dateTime': date.isoformat(),
                'timeZone': 'America/Los_Angeles',
                       },
         'end': {
            'dateTime': (date + datetime.timedelta(hours=12)).isoformat(),
            'timeZone': 'America/Los_Angeles',
                }
            }

    return event

if __name__ == '__main__':
    a = choose_remoto_days(GROUPS)
    create_events(a)
