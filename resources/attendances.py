import models 

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

attendances = Blueprint('attendances', 'attendances')

@attendances.route('/', methods=['GET'])
def attendances_index():
	attendances = models.Attendance.select()
	attendance_dicts = [ model_to_dict(attendance) for attendance in attendances]

	print(attendance_dicts)

	return jsonify({
		'data': attendance_dicts,
		'message': f"Found {len(attendance_dicts)} events.",
		'status': 200
	}), 200