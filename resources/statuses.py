import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required




statuses = Blueprint('statuses', 'statuses')




@statuses.route('/', methods=['GET'])
@login_required
def statuses_index():
	#Get all the statuses here from the database. MVP. 
	statuses = models.Status.select()
	status_dicts = [ model_to_dict(status) for status in statuses ]

	for status_dict in status_dicts:
		status_dict['user'].pop('password')

	print(status_dicts)

	return jsonify({
		'data': status_dicts,
		'message': f"Found {len(status_dicts)} statuses.",
		'status': 200
	}), 200

@statuses.route('/<eventid>', methods=['POST'])
@login_required
def create_status(eventid):
	payload = request.get_json()
	new_status = models.Status.create(
		status=payload['status'],
		user=current_user.id,
		event=eventid
	)

	status_dict = model_to_dict(new_status)

	print("Here is status_dict:")
	print(status_dict)

	status_dict['user'].pop('password')

	return jsonify(
		data=status_dict,
		message="Created a status.",
		status=201
	), 201

@statuses.route('/<id>', methods=['DELETE'])
@login_required
def delete_status(id):
	try:
		status_to_delete = models.Status.get_by_id(id)
		if status_to_delete.user.id == current_user.id:
			status_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Deleted status with id: {id}.",
				status=200
			), 200
		else:

			return jsonify(
				data={ 'error': '403 Forbidden' },
				message="User's id does not match status' id. Cannot delete.",
				status=403
			), 403
	except models.DoesNotExist:

		return jsonify(
			data={ 'error': '404 not found' },
			message="No existing status with that id.",
			status=404
		), 404

@statuses.route('/<id>', methods=['PUT'])
@login_required
def update_status(id):
	payload = request.get_json()
	status_to_update = models.Status.get_by_id(id)
	if status_to_update.user.id == current_user.id:

		if 'status' in payload:
			status_to_update.status = payload['status']

		status_to_update.save()
		updated_status_dict = model_to_dict(status_to_update)

		updated_status_dict['user'].pop('password')

		return jsonify(
			data=updated_status_dict,
			message=f"Updated status with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '403 Forbidden' },
			message="User's id does not match status' id. Cannot update.",
			status=403
		), 403

@statuses.route('/<id>', methods=['GET'])
def show_status(id):
	status = models.Status.get_by_id(id)
	if status.user.id == current_user.id:
		status_dict = model_to_dict(status)
		status_dict['user'].pop('password')
		
		return jsonify(
			data=status_dict,
			message=f"Found status with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '404 not found' },
			message="You do not have access to this information.",
			status=404
		), 404