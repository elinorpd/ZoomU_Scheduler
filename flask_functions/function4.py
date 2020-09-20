
#first, create the events for the completely synchronous classes
for name in synch:
    print(name)
    service.events().insert(calendarId=new_calendar_id, body=event_dic[name]).execute()

def freebusy():
    dt1 = home_tz.localize(dt(2020, 9, 21, 12))
    dt2 = home_tz.localize(dt(2020, 9, 22, 12))
    body = {"kind":"calendar#freeBusy",
      "timeMin": dt1.isoformat(), # in future need tp have it do next monday to next sunday
      "timeMax": dt2.isoformat(),
      "timeZone": 'Europe/Moscow',
      "items": [
        {
          "id": new_calendar_id
        }
      ]
    }

    free = service.freebusy().query(body=body).execute()
    return free

    free = freebusy()

#next, set a sleep time

times_list = []
class_starts = []
class_ends = []
for dic in free['calendars'][new_calendar_id]['busy']:
    print(dic)
    #get the intervals as datetime
    times_list.append(dic['start'])
    class_starts.append(dic['start'])
    times_list.append(dic['end'])
    class_ends.append(dic['end'])

times_list.sort()
times_list = [dt.strptime(time[0:-6],'%Y-%m-%dT%H:%M:%S') for time in times_list]
#class_starts = [dt.strptime(time[0:-6],'%Y-%m-%dT%H:%M:%S') for time in class_starts]
#class_ends = [dt.strptime(time[0:-6],'%Y-%m-%dT%H:%M:%S') for time in class_ends]
class_starts = [int(time[11:13]) for time in class_starts]
class_ends = [int(time[11:13]) for time in class_ends]

try:
    latest_class = max(i for i in class_ends if i <= 5)
except:
    latest_class = max(class_ends)

earliest_class = min(i for i in class_starts if i >= 5)


def make_sleep_event():
    event = { #need to add recurrence!
          'summary': 'Sleept',
          'description': 'zzzzzz',
        'recurrence': ['RRULE:FREQ=DAILY'],
          'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Europe/Moscow',
          },
          'end': {
            'dateTime': stop_datetime.isoformat(),
            'timeZone': 'Europe/Moscow',
          }
        }
    event = service.events().insert(calendarId=new_calendar_id, body=event).execute()

if time_of_day == 0: #if morning person
    #find the sleep start time that's 10 pm or 1 hr after your last class, whichever is earlier
    if latest_class <= 21 and latest_class >= 12:
        #sleep at 22
        start_datetime = dt(2020, 9, 21, 22)
        stop_datetime = dt(2020, 9, 22, (22+sleep_time)%24)
        make_sleep_event()
    else:
        #sleep at latest_class+1
        if latest_class <= 5:
            start_datetime = dt(2020, 9, 22, latest_class+1) #this would be so much easier achieved w datetimes ngl
        else:
            start_datetime = dt(2020, 9, 21, latest_class+1)
        stop_datetime = dt(2020, 9, 22, (latest_class+1+sleep_time)%24)
        make_sleep_event()
else: #if night owl
    #find the sleep start that ends at 12 pm or an hour before earliest class, whichever is later
    if earliest_class >= 13:
        #sleep until 12
        start_datetime = dt(2020, 9, 22, 12-sleep_time)
        stop_datetime = dt(2020, 9, 22, 12)
        make_sleep_event()
    else:
        start_datetime = dt(2020, 9, 22, earliest_class-1-sleep_time)
        stop_datetime = dt(2020, 9, 22, earliest_class-1)
        make_sleep_event()
