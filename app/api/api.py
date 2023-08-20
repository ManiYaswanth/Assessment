from flask import Blueprint, request, render_template, json, jsonify, abort

from db_models.db import TRACKING_PLAN, EVENTS, EVENT_TRACKING_MAP

import traceback

mod = Blueprint("api", __name__, template_folder="templates")

@mod.route('/tracking_plans', methods=['POST'])
def create_tracking_plan():
    data = request.json
    if not data:
        return jsonify(message="Invalid request"), 400
    client_msg = ""
    display_name = data['tracking_plan']['display_name']

    events_data = data['tracking_plan']['rules'].get('events', [])

    tracking_plan_id = max(TRACKING_PLAN, key= lambda x: x) + 1 if TRACKING_PLAN else 1

    TRACKING_PLAN[tracking_plan_id] = {"display_name": display_name, "events": [event["name"] for event in events_data]}
    client_msg += f"tracking_plan with id = {tracking_plan_id} has been added"

    for event in events_data:
        if EVENTS.get(event["name"]):                  # validation for event rules and description for existing event
            client_msg += f'Event: {event["name"]} already exists'
        else:
            EVENTS[event["name"]] = {"name": event["name"], "description": event["description"], "rules": event["rules"]}
            client_msg += f'Event: {event["name"]} has been created'

        if EVENT_TRACKING_MAP.get(event["name"]):
            if not tracking_plan_id in EVENT_TRACKING_MAP[event["name"]]:
                EVENT_TRACKING_MAP[event["name"]].append(tracking_plan_id)  
        else:
            EVENT_TRACKING_MAP[event["name"]] = [tracking_plan_id] 

        client_msg += f'Event: {event["name"]} linked to tracking_plan  with id={tracking_plan_id}'

    return jsonify(message=client_msg), 201


@mod.route('/tracking_plans/<tracking_plan_id>', methods=['GET'])
def get_tracking_plan(tracking_plan_id):
    tracking_plan = TRACKING_PLAN.get(int(tracking_plan_id))
    if not tracking_plan:
        return jsonify(error='Tracking plan not found'), 404
    return jsonify(id=tracking_plan_id, display_name=tracking_plan["display_name"], events=tracking_plan["events"])


@mod.route('/tracking_plans/<tracking_plan_id>', methods=['PUT'])
def update_tracking_plan(tracking_plan_id):
    tracking_plan = TRACKING_PLAN.get(int(tracking_plan_id))
    if not tracking_plan:
        return jsonify(error='Tracking plan not found'), 404
    data = request.json
    previous_events = tracking_plan["events"]
    
    tracking_plan["display_name"] = data['display_name']
    tracking_plan["events"] = data['events']                        # array of event names if new event create event

    for event in previous_events:
        if tracking_plan_id in EVENT_TRACKING_MAP[event]:
            EVENT_TRACKING_MAP[event].remove(tracking_plan_id)   # detach tracking plan from previous event

    for event in data["events"]:
        if not tracking_plan_id in EVENT_TRACKING_MAP[event]:
            EVENT_TRACKING_MAP[event].append(tracking_plan_id)    # attach tracking plan to event
    
    return jsonify(message='Tracking plan updated successfully')



@mod.route('/event', methods=['POST'])
def create_event():
    event = request.json        #validation for existing event
    EVENTS[event["name"]] = {"name": event["name"], "description": event["description"], "rules": event["rules"]}
   
    return jsonify(message=f'Event {event["name"]} created successfully'), 201

@mod.route('/events/<event_name>', methods=['GET'])
def get_event(event_name):
    event = EVENTS.get(event_name)
    if not event:
        return jsonify(error='Event not found'), 404
    return jsonify(name=event["name"], description=event["description"], rules=event["rules"]), 200

@mod.route('/events/<event_name>', methods=['PUT'])
def update_event(event_name):
    event = EVENTS.get(event_name)
    if not event:
        return jsonify(error='Event not found'), 404
    data = request.json

    event["description"] = data.get('description')
    event["rules"] = data['rules']
    return jsonify(message='Event updated successfully'), 200

@mod.route('/home', methods=['GET'])
def render_home():
    return render_template("home.html")

@mod.route('/save_tracking_plans', methods=['POST'])
def save_tracking_plan():
    data = request.json
    if not data:
        abort(404)
    client_msg = ""
    display_name = data['name']
    description = data["description"]
    events_data = data.get('events', [])
    tracking_plan_id = max(TRACKING_PLAN, key= lambda x: x) + 1 if TRACKING_PLAN else 1
    TRACKING_PLAN[tracking_plan_id] = {"display_name": display_name, "description": description, "events": [event["name"] for event in events_data]}
    client_msg += f"tracking_plan with id = {tracking_plan_id} has been added"

    for event in events_data:
        if EVENTS.get(event["name"]):
            client_msg += f'Event: {event["name"]} already exists'
        else:
            EVENTS[event["name"]] = {"name": event["name"], "description": event["description"], "rules": event["rules"]}
            client_msg += f'Event: {event["name"]} has been created'

        if EVENT_TRACKING_MAP.get(event["name"]):
            EVENT_TRACKING_MAP[event["name"]].append(tracking_plan_id)
        else:
            EVENT_TRACKING_MAP[event["name"]] = [tracking_plan_id]

        client_msg += f'Event: {event["name"]} linked to tracking_plan  with id={tracking_plan_id}'
    print(EVENT_TRACKING_MAP, EVENTS, TRACKING_PLAN)

    return jsonify(message=client_msg), 201