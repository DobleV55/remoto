from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from calendar import Calendar
from collections import defaultdict
from progress.bar import Bar
import datetime
import pickle
import os.path
import pprint
import random
import time
import click

GROUP0 = ['employee0', 'employee1']

GROUP1 = ['employee2', 'employee3']

GROUP2 = ['employee4', 'employee5']

GROUP3 = ['employee7', 'employee6']

GROUPS = [GROUP0, GROUP1, GROUP2, GROUP3]

def menu(month, year, current_month_days):
    menu_options = ['1. Start', '0. Exit']    
    print (menu_options)
    option = click.prompt('Choose an option', type=int)
    if option == 1:
        a = choose_remoto_days(GROUPS, current_month_days)
        create_events(a)
    if option == 0:
        print('Bye Bye!')
        exit()
    else:
        return menu(month, year, current_month_days)

def choose_remoto_days(groups, current_month_days): 
    first_half = current_month_days[:int((len(current_month_days)/2))]
    second_half = current_month_days[int((len(current_month_days)/2)):]
    res = {}
    random.shuffle(first_half)
    usados = defaultdict(int)
    for members in GROUPS:
        aux = first_half.copy()
        aux2 = second_half.copy()
        for member in members:
            remoto_1 = aux.pop(random.randrange(len(aux)))
            usados[remoto_1] += 1
            if usados[remoto_1] == 3:
                first_half.remove(remoto_1)
            remoto_2 = aux2.pop(random.randrange(len(aux2)))
            usados[remoto_2] += 1
            if usados[remoto_2] == 3:
                second_half.remove(remoto_2)
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
                'credentials.json', SCOPES)
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

@click.command()
@click.option('--month', default=9, prompt='month')
@click.option('--year', default=2019, prompt='year',
              help='The person to greet.')

def main(month, year):
    current_month_days = [day for day in Calendar().itermonthdates(year, month) if day.weekday() not in [5,6] and day.month == month]
    menu(month, year, current_month_days)

if __name__ == '__main__':
    main()
