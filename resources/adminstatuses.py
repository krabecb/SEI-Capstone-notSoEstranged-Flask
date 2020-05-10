import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required




adminstatuses = Blueprint('adminstatuses', 'adminstatuses')




@adminstatuses.route('/', methods=['GET'])
@login_required
def adminstatuses_index():
	current_user_adminstatus_dicts = [model_to_dict(adminstatus) for adminstatus in current_user.adminstatuses]

	for adminstatus_dict in current_user_adminstatus_dicts:
		adminstatus_dict['admin'].pop('password')

	print(current_user_adminstatus_dicts)

	return jsonify({
		'data': current_user_adminstatus_dicts,
		'message': f"Found {len(current_user_adminstatus_dicts)} statuses.",
		'status': 200
	}), 200

@adminstatuses.route('/', methods=['POST'])
@login_required
def create_adminstatus():
	payload = request.get_json()
	new_adminstatus = models.AdminStatus.create(
		status=payload['status'],
		admin=current_user.id
	)

	adminstatus_dict = model_to_dict(new_adminstatus)

	print(adminstatus_dict)

	adminstatus_dict['admin'].pop('password')

	return jsonify(
		data=adminstatus_dict,
		message="Created a status.",
		status=201
	), 201

@adminstatuses.route('/<id>', methods=['DELETE'])
@login_required
def delete_adminstatus(id):
	try:
		adminstatus_to_delete = models.AdminStatus.get_by_id(id)
		if adminstatus_to_delete.admin.id == current_user.id:
			adminstatus_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Deleted status with id: {id}.",
				status=200
			), 200
		else:

			return jsonify(
				data={ 'error': '403 Forbidden' },
				message="Admin's id does not match status' id. Cannot delete.",
				status=403
			), 403
	except models.DoesNotExist:

		return jsonify(
			data={ 'error': '404 not found' },
			message="No existing status with that id.",
			status=404
		), 404

@adminstatuses.route('/<id>', methods=['PUT'])
@login_required
def update_adminstatus(id):
	payload = request.get_json()
	adminstatus_to_update = models.AdminStatus.get_by_id(id)
	if adminstatus_to_update.admin.id == current_user.id:

		if 'status' in payload:
			adminstatus_to_update.status = payload['status']

		adminstatus_to_update.save()
		updated_adminstatus_dict = model_to_dict(adminstatus_to_update)

		updated_adminstatus_dict['admin'].pop('password')

		return jsonify(
			data=updated_adminstatus_dict,
			message=f"Updated status with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '403 Forbidden' },
			message="Admin's id does not match status' id. Cannot update.",
			status=403
		), 403

@adminstatuses.route('/<id>', methods=['GET'])
def show_adminstatus(id):
	adminstatus = models.AdminStatus.get_by_id(id)
	if adminstatus.admin.id == current_user.id:
		adminstatus_dict = model_to_dict(adminstatus)
		adminstatus_dict['admin'].pop('password')
		
		return jsonify(
			data=adminstatus_dict,
			message=f"Found status with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '404 not found' },
			message="You do not have access to this information.",
			status=404
		), 404