from cs50 import SQL

db = SQL("sqlite:///roster.db")

from datetime import datetime, timedelta

start = datetime.strptime("30-07-2018", "%d-%m-%Y")
end = datetime.strptime("05-08-2018", "%d-%m-%Y")

# Create dict of dates for specified range
numDays = (end-start).days + 1
dates = [dict() for x in range(0, numDays)]
for x in range(0, numDays):
    date = start + timedelta(days=x)
    dates[x]["date"] = date
    dates[x]["dateISO"] = date.strftime("%Y-%m-%d")
    dates[x]["datePretty"] = date.strftime("%d/%m/%Y")
    dates[x]["day"] = date.strftime("%A")

print(dates)



rows = db.execute('SELECT date FROM "shifts" WHERE user_id="1"')

print(rows)

shifts = db.execute("SELECT shifts.*, users.real_name FROM 'shifts' JOIN 'users' ON shifts.user_id = users.id WHERE (date BETWEEN :s AND :e)", s=start.strftime("%Y-%m-%d"), e=end.strftime("%Y-%m-%d"))

next((item for item in shifts if item["user_id"] == 1), None)

print(shifts)

#day_test = date_generated[0].strftime("%Y-%m-%d")

#test = db.execute('SELECT date FROM "shifts" WHERE user_id="1" AND date= :d', d=day_test)
#list(filter(lambda user: user['user_id'] == 1, test))
#next((test for test in test if test["user_id"] == 1), None)
next((shift for shift in shifts if (shift['date'] == dates[0]['dateISO']) and (shift['user_id'] == 1)), None)
list((shift for shift in shifts if  (shift['user_id'] == 1)))

if (next((shift for shift in shifts if (shift['date'] == dates[0]['dateISO']) and (shift['user_id'] == 1)), None)):
    print('MATCH')
else:
    print('NO MATCH')