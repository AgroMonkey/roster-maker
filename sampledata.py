from cs50 import SQL
from datetime import datetime, timedelta
import random

db = SQL("sqlite:///roster.db")


def generateSampleShifts(input_start_date, input_end_date):
    """ Generates Sample Shifts for each user for given date range"""
    start = datetime.strptime(input_start_date, "%Y-%m-%d")
    end = datetime.strptime(input_end_date, "%Y-%m-%d")

    # Create dict of dates for specified range
    numDays = (end - start).days + 1
    dates = [dict() for x in range(0, numDays)]
    for x in range(0, numDays):
        date = start + timedelta(days=x)
        dates[x]["dateISO"] = date.strftime("%Y-%m-%d")

    # Sample Data to be used
    locations = ['checkouts', 'service', 'supervisor']
    shifts = [{'start_time': '09:00', 'end_time': '13:00'},
              {'start_time': '13:00', 'end_time': '17:00'},
              {'start_time': '09:00', 'end_time': '17:00', 'break': '1hr'},
              {'start_time': '10:00', 'end_time': '16:00', 'break': '30min'},
              {'start_time': '10:00', 'end_time': '14:00'}]

    users = db.execute("SELECT id FROM 'users'")

    # Create random shifts for each user
    for user in users:
        for date in dates:
            if bool(random.getrandbits(1)):
                location = random.choice(locations)
                shift = random.choice(shifts)
                start_time = shift['start_time']
                end_time = shift['end_time']
                # Insert row into database table
                if 'break' in shift:
                    result = db.execute("INSERT INTO 'shifts' ('date', 'start_time', 'end_time', 'break', 'location', 'user_id') VALUES (:d, :s, :e, :b, :l, :u)",
                                        d=date['dateISO'], s=start_time, e=end_time, b=shift['break'], l=location, u=user['id'])
                else:
                    result = db.execute("INSERT INTO 'shifts' ('date', 'start_time', 'end_time', 'location', 'user_id') VALUES (:d, :s, :e, :l, :u)",
                                        d=date['dateISO'], s=start_time, e=end_time, l=location, u=user['id'])
                # Print out inserted data
                msg = "User: " + str(user['id']) + " "
                msg += "Date: " + date["dateISO"] + " "
                msg += "Location: " + location + " "
                msg += "Shift time: " + start_time + "-" + end_time + " "
                print(msg)


generateSampleShifts("2018-08-13", "2019-12-31")