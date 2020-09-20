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
    flow = InstalledAppFlow.from_client_secrets_file('masha_credentials.json', SCOPES)
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
    course_sync_pref = [int(request.form['course1']),int(request.form['course2']), int(request.form['course3']), int(request.form['course4']), int(request.form['course5'])]
    #create a dictionary where each entry is class_name:{dic of its atributes from user input}
    user_dic = {}
    #create a dictionary where each entry is class_name:{event params from gcal import minus event id}
    event_dic = {}
    cnt0 = 0
    for course in result['items']:
        user_dic[course['summary']]={'sync':course_sync_pref[cnt]}
        event_dic[course['summary']]= copy.deepcopy(course)
        cnt0 += 1
        try:
            del event_dic[course['summary']]['id']#remove the event id bc that's specific to this calendar and i just need the event parameters
            del event_dic[course['summary']]['htmlLink']
            del event_dic[course['summary']]['iCalUID']
            del event_dic[course['summary']]['etag']
            del event_dic[course['summary']]['organizer']
            del event_dic[course['summary']]['recurringEventId']
        except KeyError:
            pass
        except:
            break
    return render_template('creating.html')


