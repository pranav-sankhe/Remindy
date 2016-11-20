from __future__ import print_function
import httplib2
import os
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import re

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar'

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


#Input format: Set a reminder on 10 jan 2017 at 10.30pm for a date   
#key words are on, at and for 
input_string = str(raw_input())

months = ['jan', 'feb', 'march', 'apr','may','june','july','aug','sep','oct','nov','dec']

def get_credentials():
    """Gets valid user credentials from storage.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def start_datetime():
  date_str1 = input_string.split(" on ")[1].split(" at ")[0]
  date_list = date_str1.split()
  month = months.index((date_list[1]))
  year = date_list[2]
  day = date_list[0]

  time = input_string.split(" at ")[1].split(" for ")[0]
  time_val = re.findall('\d+', time)
  hours = time_val[0]
  minutes = time_val[1]

  am_pm = re.findall('\D+', time)[1]
  if am_pm == 'pm':
    time_val = str(int(hours) + 12)
  return(year + '-' + str(month+1) + '-' + day + 'T' + hours + ':' + minutes + ':00' )

def end_datetime():
  date_str1 = input_string.split(" on ")[1].split(" at ")[0]
  date_list = date_str1.split()
  month = months.index((date_list[1]))
  year = date_list[2]
  day = date_list[0]

  time = input_string.split(" at ")[1].split(" for ")[0]
  time_val = re.findall('\d+', time)
  hours = time_val[0]
  minutes = time_val[1]

  am_pm = re.findall('\D+', time)[1]
  if am_pm == 'pm':
    time_val = str(int(hours) + 12)  
  return(year + '-' + str(month+1) + '-' + day + 'T' + hours + ':' + str(int(minutes)+10) + ':00' )

def location ():
      print("enter the location:")
      val = str(raw_input())
      return val

def description ():
      print("Description:")
      val = str(raw_input())
      return val

def share():
      print("enter the mail ids of people with whom you want to share this event:")
      ids = []
      ids = str(raw_input())
      return ids

def summary():
      return input_string.split(" for ")[1]

def more_details():
      print("Want to add more details?")
      val = str(raw_input())
      if(val == 'yes' |'y'|'yup'):
        print("1. Location")
        print("2. people with whom you want to share this event")
        print("3. Add a small description of the event")
        print("4. customize the frequncy of alarms")
        print("enter the option no.s") 
        option = []
        option = input()

        for i in option: 
          if i == 1:
            location()
          if i ==2:
            share()
          if i == 3:
            alarm_freq()
        
        else:
          pass

      
def main():
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http)

  now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
  event = {
  
  'summary': summary(),
  'location': location(),
  'description': description(),
 
  'start': {
  'dateTime': start_datetime(),
  'timeZone': 'Asia/Kolkata',
   },
  
  'end': {
  'dateTime': end_datetime(),
  'timeZone': 'Asia/Kolkata'}
  ,

 'recurrence': [
  'RRULE:FREQ=DAILY;COUNT=1'
  ],

  
  'reminders': {
  'useDefault': False,
  'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
  event = service.events().insert(calendarId='primary', body=event).execute()
  print ("Event created: ")
  print (event.get('htmlLink'))
if __name__ == '__main__':
  main()


