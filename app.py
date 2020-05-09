from flask import Flask, jsonify

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




if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)