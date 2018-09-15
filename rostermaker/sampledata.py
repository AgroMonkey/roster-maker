from rostermaker import db, User, Shift
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import random
import re


def main():
    # Reset database
    do_reset = ''
    while do_reset not in ('y', 'Y', 'n', 'N'):
        do_reset = input("Do you want to reset database? (Y/N): ")
    if do_reset in ('Y', 'y'):
        print("Resetting database.")
        db.drop_all()
        db.create_all()
    else:
        print("Not resetting database.")

    # User generation
    do_users = ''
    while do_users not in ('y', 'Y', 'n', 'N'):
        do_users = input("Do you want to generate users? (Y/N): ")
    if do_users in ('Y', 'y'):
        print("Generating users.")
        generateSampleUsers()
    else:
        print("Not generating users.")

    # Shift generation
    do_shifts = ''
    while do_shifts not in ('y', 'Y', 'n', 'N'):
        do_shifts = input("Do you want to generate shifts? (Y/N): ")
    if do_shifts in ('Y', 'y'):
        print('Please enter date range')
        regex = re.compile('^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$')
        while True:
            start_date = input('Start Date (YYYY-MM-DD): ')
            if regex.match(start_date):
                break
            print("INVALID Date entered.")
        while True:
            end_date = input('End Date   (YYYY-MM-DD): ')
            if regex.match(end_date):
                break
            print("INVALID Date entered.")
        print("Generating shifts")
        generateSampleShifts(start_date, end_date)
    else:
        print("Not generating shifts")


def generateSampleUsers():
    pwd = generate_password_hash('david')
    user_1 = User('david', 'david@hotmail.com', pwd, 'David', 'admin')
    pwd = generate_password_hash('bruce')
    user_2 = User('bruce', 'bruce@test.com', pwd, 'Bruce', 'employee')
    pwd = generate_password_hash('linda')
    user_3 = User('linda', 'linda@test.com', pwd, 'Linda', 'manager')
    pwd = generate_password_hash('jason')
    user_4 = User('jason', 'jason@email.com', pwd, 'Jason', 'employee')
    pwd = generate_password_hash('rochelle')
    user_5 = User('rochelle', 'rochelle@email.com', pwd, 'Rochelle', 'manager')
    pwd = generate_password_hash('jester')
    user_6 = User('jester', 'jester@doggo.com', pwd, 'Jester', 'admin')
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.add(user_4)
    db.session.add(user_5)
    db.session.add(user_6)
    db.session.commit()


def generateSampleShifts(input_start_date, input_end_date):
    """ Generates Sample Shifts for each user for given date range"""
    start = datetime.strptime(input_start_date, "%Y-%m-%d")
    end = datetime.strptime(input_end_date, "%Y-%m-%d")

    # Create dict of dates for specified range
    numDays = (end - start).days + 1
    dates = [dict() for x in range(0, numDays)]
    for x in range(0, numDays):
        date = start + timedelta(days=x)
        dates[x]["date"] = date
        dates[x]["dateISO"] = date.strftime("%Y-%m-%d")

    # Sample Data to be used
    locations = ['checkouts', 'service', 'supervisor']
    shifts = [{'start_time': '09:00', 'end_time': '13:00'},
              {'start_time': '13:00', 'end_time': '17:00'},
              {'start_time': '09:00', 'end_time': '17:00', 'break': '1hr'},
              {'start_time': '10:00', 'end_time': '16:00', 'break': '30min'},
              {'start_time': '10:00', 'end_time': '14:00'}]

    users = User.query.with_entities(User.id)

    for user in users:
        for date in dates:
            if bool(random.getrandbits(1)):
                location = random.choice(locations)
                shift = random.choice(shifts)
                start_time = shift['start_time']
                end_time = shift['end_time']
                # Insert row into database table
                new_shift = Shift(date['date'], start_time, end_time, location, user.id)
                if 'break' in shift:
                    new_shift.sbreak = shift['break']
                db.session.add(new_shift)
                db.session.commit()

                # Print out inserted data
                msg = "User: " + str(user.id) + " "
                msg += "Date: " + date["dateISO"] + " "
                msg += "Location: " + location + " "
                msg += "Shift time: " + start_time + "-" + end_time + " "
                print(msg)


if __name__ == "__main__":
    main()
