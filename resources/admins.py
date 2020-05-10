import models 

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user




admins = Blueprint('admins', 'admins')




@admins.route('/', methods=['GET'])
def test_admin_resource():
	return "admin resource works!"

@admins.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()
	payload['password'] = payload['password'].lower()
	payload['date_of_birth'] = payload['date_of_birth']
	payload['adress'] = payload['address'].lower()
	payload['phone_number'] = payload['phone_number']
	payload['emergency_contact'] = payload['emergency_contact'].lower()
	payload['about_me'] = payload['about_me'].lower()
	print(payload)

	try:
		models.Admin.get(models.Admin.email == payload['email'])

		return jsonify(
			data={},
			message=f"An admin with {payload['email']} already exists",
			status=401
		), 401

	except models.DoesNotExist:
		pw_hash = generate_password_hash(payload['password'])

		created_admin = models.Admin.create(
			email=payload['email'],
			username=payload['username'],
			password=pw_hash,
			date_of_birth=payload['date_of_birth'],
			address=payload['address'],
			phone_number=payload['phone_number'],
			emergency_contact=payload['emergency_contact'],
			about_me=payload['about_me']
		)

		print(created_admin)

		login_user(created_admin)

		created_admin_dict = model_to_dict(created_admin)
		print(created_admin_dict)
		print(type(created_admin_dict['password']))
		created_admin_dict.pop('password')

		return jsonify(
			data=created_admin_dict,
			message=f"Successfully created admin {created_admin_dict['username']}!",
			status=201
		), 201

@admins.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	payload['password'] = payload['password'].lower()

	try:
		admin = models.Admin.get(models.Admin.username == payload['username'])
		admin_dict = model_to_dict(admin)
		password_is_good = check_password_hash(admin_dict['password'], payload['password'])

		if(password_is_good):
			login_user(admin)
			print(model_to_dict(admin))
			admin_dict.pop('password')

			return jsonify(
				data=admin_dict,
				message=f"Successfully logged in as {admin_dict['username']}.",
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
@admins.route('/all', methods=['GET'])
def admin_index():
	admins = models.Admin.select()
	admin_dicts = [ model_to_dict(admin) for admin in admins ]

	for admin_dict in admin_dicts:
		admin_dict.pop('password')

		print(admin_dicts)

		return jsonify(admin_dicts), 200

"""SHOWS WHO IS LOGGED IN"""
@admins.route('/logged_in_admin', methods=['GET'])
def get_logged_in_admin():
	print(current_admin)
	print(type(current_admin))

	if not current_admin.is_authenticated:
		return jsonify(
			data={},
			message="Currently no one is logged in",
			status=401
		), 401

	else:
		admin_dict = model_to_dict(current_admin)
		admin_dict.pop('password')

		return jsonify(
			data=admin_dict,
			message=f"{admin_dict['username']} is currently logged in.",
			status=200
		), 200

@admins.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data={},
		message="Successfully logged out.",
		status=200
	), 200