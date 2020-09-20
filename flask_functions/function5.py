for name in semisynch:
    print(name)
    print(event_dic[name]['start'], event_dic[name]['end'])
    start_time = str(event_dic[name]['start']['dateTime'])[11:16]
    end_time = str(event_dic[name]['end']['dateTime'])[11:16]

    free = {}
    we_good = True
    for i in range(21,22):
        #test that yuo're not busy any day at that time
        dt1 = school_tz.localize(dt(2020, 9, i, int(start_time[0:2]), int(start_time[3:5])))
        dt2 = school_tz.localize(dt(2020, 9, i, int(end_time[0:2]), int(end_time[3:5])))
        print(dt1,dt2)
        body = {"kind":"calendar#freeBusy",
          "timeMin": dt1.isoformat(), #need tp have it do next monday to next sunday
          "timeMax": dt2.isoformat(),
          "timeZone": 'America/New_York',
          "items": [
            {
              "id": new_calendar_id
            }
          ]
        }

        free = service.freebusy().query(body=body).execute()

        if not free['calendars'][new_calendar_id]['busy']==[]:
            asynch.append(name)
            we_good = False
            break

    if we_good:
        service.events().insert(calendarId=new_calendar_id, body=event_dic[name]).execute()
