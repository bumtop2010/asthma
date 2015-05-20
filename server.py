""" Every Breath of the Way """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Attack, AttackSymptom, Symptom, AttackTrigger, PossibleTrigger
import datetime

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key = "wheezer"

@app.route('/')
def index():
	"""Site Homepage."""


	return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def register_form():
	"""Show form for profile creation."""

	return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
	"""Process Registration."""

	unprocessed_email = request.form["email"]
	email = unprocessed_email.lower()
	first_name = request.form["first"]
	last_name = request.form["last"]
	password = request.form["password"]
	age = int(request.form["age"])

	new_user = User(email=email, first_name=first_name, last_name=last_name, password=password, age=age)

	db.session.add(new_user)
	db.session.commit()

	flash("User Profile %s added." % email)
	return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
	"""Show login form"""

	return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
	"""Process the User's login."""

	unprocessed_email = request.form["email"]
	email = unprocessed_email.lower()
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	if not user:
	    flash("Password not found. Please Register.")
	    return redirect("/login")

	if user.password != password:
	    flash("Incorrect password")
	    return redirect("/login")

	session["user_id"] = user.user_id

	flash("Logged in")
	return redirect("/user/%s" % user.user_id)

@app.route("/user/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""
    user = User.query.get(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/attack", methods=["GET"])
def attack_form():
	""" Show attack input form."""
	return render_template("attack_submission.html")

@app.route("/attack", methods=['POST'])
def attack_process():
	"""Process the User's attack."""
	
	# date = request.form["date"]
	# location = request.form["location"]


	# today = datetime.date.now()
	
	
	
	# use
	# print request.form.getlist("trigger")
	# print request.form.getlist("symptom")
	# print request.form["location"]
	# dont
	# print location

	# location = request.form["location"]
	# works with this	
	# attack_possible_triggers = request.form.getlist("trigger")
	# symptom_type_name = request.form.getlist("symptom")
	# do not uncomment
	# new_attack_triggers = PossibleTrigger(trigger=attack_possible_triggers)
	# new_attack = Attack(attack_location=location)
	# new_attack_symptoms = Symptom(symptom=symptom_type_name)
	# use
	flash("Attack added.")
	return render_template("attack_info.html")



@app.route('/list')
def attack_list():
	"""Show list of Asthma Attacks."""

	attack = Attack.query.orderby("attack_id").all()
	return render_template("list_user_attacks.html", attacks=attacks)

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


if __name__ == "__main__":
	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run()