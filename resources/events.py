import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required




events = Blueprint('events', 'events')




@events.route('/', methods=['GET'])
@login_required
def events_index():
	events = models.Event.select()
	event_dicts = [ model_to_dict(event) for event in events]

	print(event_dicts)

	return jsonify({
		'data': event_dicts,
		'message': f"Found {len(event_dicts)} events.",
		'status': 200
	}), 200

@events.route('/', methods=['POST'])
@login_required
def create_event():
	payload = request.get_json()
	new_event = models.Event.create(
		event_name=payload['event_name'],
		event_organizer=payload['event_organizer'],
		event_location=payload['event_location'],
		date_of_event=payload['date_of_event'],
		user=current_user.id
	)

	event_dict = model_to_dict(new_event)

	print(event_dict)

	event_dict['user'].pop('password')

	return jsonify(
		data=event_dict,
		message="Created an event.",
		status=201
	), 201

@events.route('/<id>', methods=['DELETE'])
@login_required
def delete_event(id):
	try:
		event_to_delete = models.Event.get_by_id(id)
		if event_to_delete.user.id == current_user.id:
			event_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Deleted event with id: {id}.",
				status=200
			), 200
		else:

			return jsonify(
				data={ 'error': '403 Forbidden' },
				message="User's id does not match event's id. Cannot delete.",
				status=403
			), 403
	except models.DoesNotExist:

		return jsonify(
			data={ 'error': '404 not found' },
			message="No existing event with that id.",
			status=404
		), 404

@events.route('/<id>', methods=['PUT'])
@login_required
def update_event(id):
	payload = request.get_json()
	event_to_update = models.Event.get_by_id(id)
	if event_to_update.user.id == current_user.id:

		if 'event_name' in payload:
			event_to_update.event_name = payload['event_name']
		if 'event_organizer' in payload:
			event_to_update.event_organizer = payload['event_organizer']
		if 'event_location' in payload:
			event_to_update.event_location = payload['event_location']
		if 'date_of_event' in payload:
			event_to_update.date_of_event = payload['date_of_event']

		event_to_update.save()
		updated_event_dict = model_to_dict(event_to_update)

		updated_event_dict['user'].pop('password')

		return jsonify(
			data=updated_event_dict,
			message=f"Updated event with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '403 Forbidden' },
			message="User's id does not match event's id. Cannot update.",
			status=403
		), 403

@events.route('/<id>', methods=['GET'])
def show_event(id):
	event = models.Event.get_by_id(id)
	if event.user.id == current_user.id:
		event_dict = model_to_dict(event)
		event_dict['user'].pop('password')
		
		return jsonify(
			data=event_dict,
			message=f"Found event with id: {id}.",
			status=200
		), 200
	else:

		return jsonify(
			data={ 'error': '404 not found' },
			message="You do not have access to this information.",
			status=404
		), 404