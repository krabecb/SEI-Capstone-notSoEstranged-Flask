from flask import Flask, jsonify

from resources.users import users

from resources.admins import admins

from resources.events import events

from resources.adminstatuses import adminstatuses

from resources.statuses import statuses

import models

from flask_cors import CORS 

from flask_login import LoginManager




DEBUG=True
PORT=8000




app=Flask(__name__)

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




app.register_blueprint(users, url_prefix='/api/users/')
app.register_blueprint(admins, url_prefix='/api/admins/')
app.register_blueprint(events, url_prefix='/api/events/')
app.register_blueprint(adminstatuses, url_prefix='/api/adminstatuses/')
app.register_blueprint(statuses, url_prefix='/api/statuses/')




if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)