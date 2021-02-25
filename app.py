import os
from flask import Flask, jsonify, g

from resources.users import users

from resources.events import events

from resources.statuses import statuses

from resources.attendances import attendances

import models

from flask_cors import CORS 

from flask_login import LoginManager




DEBUG=True
PORT=8000




app=Flask(__name__)

app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)

app.secret_key = "Secret string."




"""USER OBJECT LOADED WHEN USER LOGGED IN"""
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		print("Loading the following user:")
		user = models.User.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return None

"""SEND BACK JSON"""
@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
			'error': 'User not logged in'
		},
		message="You must be logged in to do that.",
		status=401
	), 401




CORS(users, origins=['http://localhost:3000', 'https://notsoestranged.herokuapp.com'], supports_credentials=True)
CORS(statuses, origins=['http://localhost:3000', 'https://notsoestranged.herokuapp.com'], supports_credentials=True)
CORS(events, origins=['http://localhost:3000', 'https://notsoestranged.herokuapp.com'], supports_credentials=True)
CORS(attendances, origins=['http://localhost:3000', 'https://notsoestranged.herokuapp.com'], supports_credentials=True)




app.register_blueprint(users, url_prefix='/api/users/')
app.register_blueprint(events, url_prefix='/api/events/')
app.register_blueprint(statuses, url_prefix='/api/statuses/')
app.register_blueprint(attendances, url_prefix='/api/attendances/')

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():
  """Connect to the db before each request"""
  # store the database as a global var in g
  print("you should see this before each request") # optional -- to illustrate that this code rus before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
  g.db = models.DATABASE
  g.db.connect()


@app.after_request # use this decorator to cause a function to run after reqs
def after_request(response):
  """Close the db connetion after each request"""
  print("you should see this after each request") # optional -- to illustrate that this code runs after each request
  g.db.close()
  return response # go ahead and send response back to client 
                  # (in our case this will be some JSON)



# ADD THESE THREE LINES -- because we need to initialize the
# tables in production too!
if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)