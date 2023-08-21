from flask import Blueprint, request, json, jsonify, abort
from views import api_ops
import traceback

mod = Blueprint("routes", __name__, template_folder="templates")

@mod.route('/tracking_plan', methods=['POST'])
def create_tracking_plan():
    '''
        Validate event if event already exists
        Create tracking plan
        Create events
        Map events to tracking plan
    '''
    data = request.json
    if not data or not data["tracking_plan"]:
        return jsonify(message="Invalid request"), 400
    
    client_msg = ""
    display_name = data['tracking_plan']['display_name']
    description = data["tracking_plan"].get("description", "")
    events_data = data['tracking_plan']['rules'].get('events', []) if data["tracking_plan"].get('rules') else []

    if not events_data:
        events_data = data["tracking_plan"].get("events", [])
    tracking_plan_id = api_ops.set_tracking_plan(display_name, description, events_data)

    for event in events_data:
        val = api_ops.validate_event(event)
        if val == "clear":
            api_ops.set_event(event)
        elif val == "error":
            return "invalid event", 400
        api_ops.set_event_tracking_mapping(tracking_plan_id, event)

    client_msg += f'tracking_plan with id={tracking_plan_id} has been created'
    return jsonify(message=client_msg), 201


@mod.route('/tracking_plans', methods=['GET'])
def fetch_all_tracking_plans():
    tracking_plans = api_ops.get_tracking_plans()
    print(f'{tracking_plans = }')
    return tracking_plans, 200


@mod.route('/tracking_plans/<tracking_plan_name>', methods=['GET'])
def fetch_tracking_plan(tracking_plan_name):
    tracking_plan = api_ops.get_tracking_plan(tracking_plan_name)
    if not tracking_plan:
        return "tracking plan doesn't exist", 404
    return tracking_plan, 200


@mod.route('/tracking_plans/<tracking_plan_name>', methods=['PUT'])
def modify_tracking_plan(tracking_plan_name):
    data = request.json
    updated_plan = api_ops.update_tracking_plan(tracking_plan_name, data["display_name"], data["events"])
    if not updated_plan:
        return "tracking plan doesn't exist", 404
    return jsonify(message='Tracking plan updated successfully')


@mod.route('/event', methods=['POST'])
def create_event():
    event = request.json
    msg = api_ops.validate_event(event)
    if msg != "clear":
        return "invalid event", 400
    api_ops.set_event(event)
    return jsonify(message=f'Event {event["name"]} created successfully'), 201


@mod.route('/events/<event_name>', methods=['GET'])
def get_event(event_name):
    event = api_ops.get_event(event_name)
    if not event:
        return jsonify(error='Event not found'), 404
    return jsonify(name=event["name"], description=event["description"], rules=event["rules"]), 200


@mod.route('/events/<event_name>', methods=['PUT'])
def modify_event(event_name):
    data = request.json
    event = api_ops.update_event(event_name, data["description"], data["rules"])
    if not event:
        return jsonify(error='Event not found'), 404
    
    return jsonify(message='Event updated successfully'), 200