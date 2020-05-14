import models 

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user




users = Blueprint('users', 'users')




@users.route('/', methods=['GET'])
def test_user_resource():
	return "user resource works!"

@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()
	payload['password'] = payload['password'].lower()
	payload['date_of_birth'] = payload['date_of_birth']
	payload['address'] = payload['address'].lower()
	payload['phone_number'] = payload['phone_number']
	payload['emergency_contact'] = payload['emergency_contact'].lower()
	payload['about_me'] = payload['about_me'].lower()
	print(payload)

	try:
		models.User.get(models.User.email == payload['email'])

		return jsonify(
			data={},
			message=f"A user with {payload['email']} already exists",
			status=401
		), 401

	except models.DoesNotExist:
		pw_hash = generate_password_hash(payload['password'])

		created_user = models.User.create(
			email=payload['email'],
			username=payload['username'],
			password=pw_hash,
			date_of_birth=payload['date_of_birth'],
			address=payload['address'],
			phone_number=payload['phone_number'],
			emergency_contact=payload['emergency_contact'],
			about_me=payload['about_me'],
			is_admin=payload['is_admin']
		)

		print(created_user)

		login_user(created_user)

		created_user_dict = model_to_dict(created_user)
		print(created_user_dict)
		print(type(created_user_dict['password']))
		created_user_dict.pop('password')

		return jsonify(
			data=created_user_dict,
			message=f"Successfully created user {created_user_dict['username']}!",
			status=201
		), 201

@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	payload['password'] = payload['password'].lower()

	try:
		user = models.User.get(models.User.username == payload['username'])
		user_dict = model_to_dict(user)
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		if(password_is_good):
			login_user(user)
			print(model_to_dict(user))
			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message=f"Successfully logged in as {user_dict['username']}.",
				status=200
			), 200
		else:
			print("Bad username or password")

			return jsonify(
				data={},
				message="Username or password is incorrect",
				status=401
			), 401
	except models.DoesNotExist:
		print('username is no good')

		return jsonify(
			data={},
			message="Username or password is incorrect",
			status=401
		), 401

"""HELPER ROUTE"""
@users.route('/all', methods=['GET'])
def user_index():
	users = models.User.select()
	user_dicts = [ model_to_dict(user) for user in users ]

	for user_dict in user_dicts:
		user_dict.pop('password')

		print(user_dicts)

		return jsonify(user_dicts), 200

"""SHOWS WHO IS LOGGED IN"""
@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
	print("Here is current_user:")
	print(current_user)
	print(type(current_user))

	if not current_user.is_authenticated:
		return jsonify(
			data={},
			message="Currently no one is logged in",
			status=401
		), 401

	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"{user_dict['username']} is currently logged in.",
			status=200
		), 200

@users.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data={},
		message="Successfully logged out.",
		status=200
	), 200

@users.route('/<c>', methods=['PUT'])
def connect_user(c):

	connect_user_to_event = models.Event.get_by_id(c)

	connected_user = models.User.get_by_id(current_user.id)

	connected_user.attending_event=connect_user_to_event.id

	connected_user.save()

	connected_user_dict = model_to_dict(connected_user)

	print(connected_user_dict)
	print("Here is connected_user:")


	return jsonify(
		data=connected_user_dict,
		message="Current user is now attending an event!",
		status=201
	), 201