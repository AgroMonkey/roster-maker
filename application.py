from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from pytz import timezone

from helpers import apology, login_required, admin_required, manager_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///roster.db")


@app.route("/")
@login_required
def index():
    """Shows index screen with next shift and notifications"""
    shifts = db.execute("SELECT * FROM 'shifts' WHERE user_id = :i AND date >= date('now') ORDER BY date LIMIT 1",
                        i=session["user_id"])
    if shifts:
        shift = shifts[0]
        date = datetime.strptime(shift["date"], "%Y-%m-%d")
        shift["datePretty"] = date.strftime("%d/%m/%Y")
        shift["day"] = date.strftime("%A")
    else:
        shift = None

    return render_template("index.html", shift=shift)


@app.route("/locations", methods=["GET"])
@app.route("/roster", methods=["GET"])
@login_required
def roster():
    """Shows roster for current week or using input range"""

    # Work out dates for Start/End of Week
    if request.args.get("start_date") and request.args.get("end_date"):
        start = datetime.strptime(request.args.get("start_date"), "%Y-%m-%d")
        end = datetime.strptime(request.args.get("end_date"), "%Y-%m-%d")
    else:
        tz = timezone('Australia/Sydney')
        today = datetime.now(tz).date()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)

    # Create dict of dates for specified range
    numDays = (end - start).days + 1
    dates = [dict() for x in range(0, numDays)]
    for x in range(0, numDays):
        date = start + timedelta(days=x)
        dates[x]["dateISO"] = date.strftime("%Y-%m-%d")
        dates[x]["datePretty"] = date.strftime("%d/%m/%Y")
        dates[x]["day"] = date.strftime("%A")

    users = db.execute("SELECT id, real_name FROM 'users' ORDER BY real_name")
    shifts = db.execute("SELECT shifts.*, users.real_name FROM 'shifts' JOIN 'users' ON shifts.user_id = users.id WHERE (date BETWEEN :s AND :e) ORDER BY start_time",
                        s=start.strftime("%Y-%m-%d"), e=end.strftime("%Y-%m-%d"))
    locations = db.execute("SELECT location FROM 'shifts' GROUP BY location")

    return render_template("roster.html", dates=dates, users=users, shifts=shifts, locations=locations)


@app.route("/deleteshift", methods=["POST"])
@manager_required
def deleteshift():
    """Delete shift from roster"""
    shift_id = request.form.get("shift_id")
    print("Deleted Shift ID: " + shift_id)
    result = db.execute("DELETE FROM shifts WHERE shift_id = :s", s=shift_id)
    if result:
        flash('Shift Succesfully Deleted')
    else:
        flash('Deletion Failed')
    return redirect(request.referrer)


@app.route("/updateroster", methods=["POST"])
@manager_required
def updateroster():
    """Update/Add shifts in roster"""
    print("Update Roster")
    if not request.form.get("user_id"):
        return apology("must provide user_id")
    if not request.form.get("date"):
        return apology("must provide date")
    if not request.form.get("location"):
        return apology("must provide location")
    if not request.form.get("start_time"):
        return apology("must provide start_time")
    if not request.form.get("end_time"):
        return apology("must provide end_time")
    if not request.form.get("break"):
        return apology("must provide break")
    user_id = request.form.get("user_id")
    date = request.form.get("date")
    location = request.form.get("location").lower()
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    if (request.form.get("break") == "None"):
        sbreak = None
    else:
        sbreak = request.form.get("break")
    if (request.form.get("shift_id")):
        shift_id = request.form.get("shift_id")
        result = db.execute("UPDATE shifts SET user_id= :u, date= :d, location= :l, start_time= :st, end_time= :e, break= :b WHERE shift_id = :si",
                            u=user_id, d=date, l=location, st=start_time, e=end_time, b=sbreak, si=shift_id)
        if result:
            return redirect(request.referrer)
        else:
            return apology("Shift Edit Failed")
    else:
        result = db.execute("INSERT INTO 'shifts' ('user_id', 'date', 'location', 'start_time', 'end_time', 'break') VALUES (:u, :d, :l, :st, :e, :b)",
                            u=user_id, d=date, l=location, st=start_time, e=end_time, b=sbreak)
        if result:
            return redirect(request.referrer)
        else:
            return apology("Add Shift Failed")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["pass"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_role"] = rows[0]["role"]
        session["user_real_name"] = rows[0]["real_name"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash('You were successfully logged out')
    return redirect("/")


@app.route("/updateuser", methods=["POST"])
@admin_required
def updateuser():
    """Add/Edit user"""

    # Ensure all fields were submitted
    if not request.form.get("username"):
        return apology("must provide username")
    elif not request.form.get("email"):
        return apology("must provide email")
    elif not request.form.get("real_name"):
        return apology("must provide real name")
    elif not request.form.get("role"):
        return apology("must provide role")

    # check if changing password or adding new user
    if request.form.get("changePass"):
        if not request.form.get("password"):
            return apology("must provide password")
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("Password and confirmation don't match")
        pwd = generate_password_hash(request.form.get("password"))

    user = request.form.get("username")
    email = request.form.get("email")
    name = request.form.get("real_name")
    role = request.form.get("role")

    if request.form.get("user_id"):
        user_id = request.form.get("user_id")
        # Editing existing user
        result = db.execute("UPDATE users SET username= :u, email= :e, real_name= :n, role= :r WHERE id = :i",
                            u=user, e=email, n=name, r=role, i=user_id)
        if not result:
            return apology("Could not edit user")
        if request.form.get("changePass"):
            # If password changing
            result2 = db.execute("UPDATE users SET pass= :p WHERE id = :i", p=pwd, i=user_id)
            if not result2:
                return apology("Could not change pass")
        flash('User succesfully modified')
        return redirect("/users")
    else:
        if not pwd:
            return apology("Missing password info")
        # Adding new user
        result3 = db.execute("INSERT INTO 'users' ('username', 'pass', 'email', 'real_name', 'role') VALUES (:u, :p, :e, :n, :r)",
                             u=user, p=pwd, e=email, n=name, r=role)
        if not result3:
            return apology("Could not create user")
        else:
            flash('User succesfully registered')
            return redirect("/users")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    """Change Password of current user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("oldpass"):
            return apology("must provide old pass")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide new pass")
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")
        # Ensure passwords match
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("Password and confirmation don't match")
        # Check if old password matches
        rows = db.execute("SELECT * FROM users WHERE id = :i", i=session["user_id"])
        if not check_password_hash(rows[0]["pass"], request.form.get("oldpass")):
            return apology("Old password doesn't match")

        pwd = generate_password_hash(request.form.get("password"))
        result = db.execute("UPDATE users SET pass= :p WHERE id = :i", p=pwd, i=session["user_id"])

        if not result:
            return apology("Could not change pass")
        else:
            # Redirect user to home page
            flash('Password succefully changed')
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepass.html")


@app.route("/users",  methods=["GET"])
@admin_required
def users():
    """Show list of users"""
    users = db.execute("SELECT * FROM 'users'")
    return render_template("users.html", users=users)


@app.route("/deleteuser",  methods=["POST"])
@admin_required
def delete_user():
    """Delete user"""
    if not request.form.get("id"):
        return apology("must provide id")
    user_id = request.form.get("id")
    result = db.execute("DELETE FROM 'users' WHERE id = :i", i=user_id)
    if not result:
        return apology("Could not delete user")
    else:
        flash('User succesfully deleted')
        return redirect("/users")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)