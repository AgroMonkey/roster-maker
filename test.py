from application import db, User, Shift
from datetime import datetime
from pytz import timezone
from werkzeug.security import check_password_hash, generate_password_hash

db.create_all()

pwd = generate_password_hash('david')
user_1 = User('david', 'david@email.com', pwd, 'David A', 'admin')
pwd = generate_password_hash('bruce')
user_2 = User('bruce', 'bruce@email.com', pwd, 'Bruce A', 'manager')
pwd = generate_password_hash('jason')
user_3 = User('jason', 'jason@test.com', pwd, 'Jason', 'employee')
db.session.add(user_1)
db.session.add(user_2)
db.session.add(user_3)
db.session.commit()

tz = timezone('Australia/Sydney')
date = datetime.now(tz).date()
date2 = datetime.strptime('2018-08-16', '%Y-%m-%d')

shift_1 = Shift(date, '09:00', '17:00', 'checkouts', '1', '1hr')
shift_2 = Shift(date, '10:00', '18:00', 'checkouts', '2', '1hr')
shift_3 = Shift(date, '09:00', '13:00', 'service', '3')

shift_4 = Shift(date2, '11:00', '18:00', 'supervisor', '1', '30min')
shift_5 = Shift(date2, '9:00', '17:00', 'service', '2', '30min')
shift_6 = Shift(date2, '13:00', '18:00', 'checkouts', '3')

db.session.add(shift_1)
db.session.add(shift_2)
db.session.add(shift_3)
db.session.add(shift_4)
db.session.add(shift_5)
db.session.add(shift_6)
db.session.commit()
