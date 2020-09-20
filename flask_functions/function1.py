from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime as dt
import pytz
import copy

#declare read/write ability
scopes = ['https://www.googleapis.com/auth/calendar']

#lowk unclear how to do this well come back to it
flow = InstalledAppFlow.from_client_secrets_file("masha_credentials.json", scopes=scopes)


#ok back to real and applicable stuff
#service is gonna be used EVERYWHERE its basically how we connect to the api
service = build("calendar", "v3", credentials=credentials)
cal_result = service.calendarList().list().execute()

def get_calendar_list():
    cnt = 0
    calendar_list = []
    for i in cal_result['items']:
        calendar_list.append(str(cnt)+' '+i['summary'])
        cnt +=1
    return calendar_list
