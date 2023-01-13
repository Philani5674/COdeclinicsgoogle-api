from __future__ import print_function

import datetime
import os.path
from sys import argv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('.token.json'):
        creds = Credentials.from_authorized_user_file('.token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.creditials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('.token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        service = build('calendar', 'v3', credentials=creds)
        calendar_list = service.calendarList().list(pageToken=None).execute() 
        for calendar_list_entry in calendar_list['items']:
            
            print(f'Getting the upcoming 7 days events for calendar of', calendar_list_entry['summary'])
            for i in range(0,7):
                # Call the Calendar API
                today = datetime.date.today() 
                timeStart = str(today+ datetime.timedelta(days=i)) + "T00:00:00Z" # 'Z' indicates UTC time
                timeEnd = str(today + datetime.timedelta(days=i)) + "T23:59:59Z" 
                
                events_result = service.events().list(calendarId=calendar_list_entry['id'], 
                                                    timeMin=timeStart, 
                                                    timeMax=timeEnd, singleEvents=True, 
                                                    orderBy='startTime', timeZone='Africa/Johannesburg').execute()

                
                events = events_result.get('items', [])
                if not events:
                    print(str(today + datetime.timedelta(days=i)),'No upcoming events found.')
                    continue
                    
                
                # Prints the start and name of the next 10 events
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z"), event['summary'])
                    
                
        
            
        
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()