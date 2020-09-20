from  __future__  import print_function
from flask import Flask, render_template, request, redirect, flash, url_for
from app import app
from app.forms import LoginForm
import datetime
import pickle
import os.path
import googleapiclient.discovery
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime as dt
import pytz
import copy




@app.route('/')
@app.route('/index')
def index():
    #print("hello world")
	user = {'username': 'Elinor'}
	posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
	return render_template('index.html', title="corndog", user=user, posts=posts)

@app.route("/cal")
def cal():
    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with  open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
    'masha_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            # with open('token.pickle', 'wb') as token: # can't write files in Google App Engine so comment out or delete
            # pickle.dump(creds, token)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    # Call the Calendar API

    #mashas code
    print('listing all calendars')
    cal_result = service.calendarList().list().execute()
    print(cal_result['items'])
    cnt = 0
    calendar_list = []
    for i in cal_result['items']:
        calendar_list.append(i['summary'])
    for i in calendar_list:
        print(cnt, i)
        cnt +=1
    

    return  render_template("cal.html", calendar_list=calendar_list)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    sleep_time = request.form['sleep']
    time_of_day = request.form['studypref']
    calendar_choice = int(request.form['gcalnum'])
    localtimezone= "UTC"+request.form['localtimezone']
    schooltimezone= "UTC"+request.form['schooltimezone']

    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with  open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
    'masha_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    cal_result = service.calendarList().list().execute()
    calendar_id = cal_result['items'][calendar_choice]['id']
    result = service.events().list(calendarId=calendar_id).execute()

    course_list = []
    for course in result['items']:
        course_list.append(course['summary'])
    print(course_list)    


    return render_template('schedule.html', calendar_choice=calendar_choice, course_list=course_list)

@app.route('/creating', methods=['GET', 'POST'])
def creating():
    

    return render_template('creating.html')


