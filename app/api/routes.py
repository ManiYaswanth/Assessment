from flask import Blueprint, request, json, jsonify, abort
from views import api_ops
from http import HTTPStatus
from exception_handlers.Exceptions import InvalidEventException, InvalidTrackingPlanException
import traceback

mod = Blueprint("routes", __name__, template_folder="templates")

@mod.route('/tracking_plan', methods=['POST'])
def create_tracking_plan():
    '''
    request:
        The JSON object containing the tracking plan and events.
    responses:
        201:
            description: tracking_plan created
    '''
    try:
        data = request.json if request.data else None
        if not data or api_ops.validate_tracking_plan(data) == "invalid":
            raise InvalidTrackingPlanException
    
        client_msg = ""
        display_name = data['tracking_plan']['display_name']
        description = data["tracking_plan"].get("description", "")
        events_data = data['tracking_plan']['rules'].get('events', []) if data["tracking_plan"].get('rules') else []
        for event in events_data:
            if api_ops.validate_event(event) == "invalid":
                raise InvalidEventException
            
        if not events_data:
            events_data = data["tracking_plan"].get("events", [])
        tracking_plan_id = api_ops.set_tracking_plan(display_name, description, events_data)

        for event in events_data:
            api_ops.set_event(event)
            api_ops.set_event_tracking_mapping(tracking_plan_id, event)

        client_msg += f'tracking_plan with id={tracking_plan_id} has been created'
        return jsonify(message=client_msg), HTTPStatus.CREATED
    except InvalidEventException as e:
        return jsonify(message = e.description), e.code
    except InvalidTrackingPlanException as e:
        return jsonify(message = e.description), e.code
    except:
        return jsonify(message="Internal Server Error"), HTTPStatus.INTERNAL_SERVER_ERROR


@mod.route('/tracking_plans', methods=['GET'])
def fetch_all_tracking_plans():
    '''
    responses:
        200:
            description: return all tracking plans
    '''
    try:
        tracking_plans = api_ops.get_tracking_plans()
        return tracking_plans, HTTPStatus.OK
    except:
        return jsonify(message ="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR


@mod.route('/tracking_plans/<tracking_plan_name>', methods=['GET'])
def fetch_tracking_plan(tracking_plan_name):
    '''
    request:
        Path parameter: tracking_plan_name
    responses:
        200:
            description: return tracking_plan with tracking_plan_name
        404:
            description: tracking plan not found
    '''
    try:
        tracking_plan = api_ops.get_tracking_plan(tracking_plan_name)
        if not tracking_plan:
            return "tracking plan not found", HTTPStatus.NOT_FOUND
        return tracking_plan, HTTPStatus.OK
    except:
        return jsonify(message ="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR


@mod.route('/tracking_plans/<tracking_plan_name>', methods=['PUT'])
def modify_tracking_plan(tracking_plan_name):
    '''
    request:
        Path parameter: tracking_plan_name
    responses:
        201:
            description: message that tracking plan is updated succesfully
        404:
            description: tracking_plan not found
    '''
    try:
        data = request.json if request.data else None
        if not data or api_ops.validate_tracking_plan(data) == "invalid":
            raise InvalidTrackingPlanException
        updated_plan = api_ops.update_tracking_plan(tracking_plan_name, data["tracking_plan"].get("description", ""), data["tracking_plan"].get("display_name", ""), data["tracking_plan"]["rules"].get("events", []))
        if not updated_plan:
            return "tracking plan doesn't exist", HTTPStatus.NOT_FOUND
        return jsonify(message='Tracking plan updated successfully')
    except InvalidTrackingPlanException as e:
        return jsonify(message =e.description), e.code
    except:
        return jsonify(message ="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR


@mod.route('/event', methods=['POST'])
def create_event():
    '''
    request:
        The JSON object containing the event.
    responses:
        201:
            description: event created
        400:
            description: Invalid event object
    '''
    try:
        event = request.json if request.data else None
        event_validation = api_ops.validate_event(event)
        if not event or event_validation == "valid":
            raise InvalidEventException
        elif event_validation == "exists":
            return jsonify(message = f"Event with {event['name']} already exists"), HTTPStatus.BAD_REQUEST 
        api_ops.set_event(event)
        return jsonify(message=f'Event {event["name"]} created successfully'), HTTPStatus.CREATED
    except InvalidEventException as e:
        return jsonify(message =e.description), e.code
    except:
        return jsonify(message ="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR


@mod.route('/events/<event_name>', methods=['GET'])
def get_event(event_name):
    '''
    request:
        path parameter: event_name.
    responses:
        200:
            description: event object
        404:
            description: event not found
    '''
    try:
        event = api_ops.get_event(event_name)
        if not event:
            return jsonify(error='Event not found'), HTTPStatus.NOT_FOUND
        return jsonify(name=event["name"], description=event["description"], rules=event["rules"]), 200
    except:
        return jsonify(message ="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR


@mod.route('/events/<event_name>', methods=['PUT'])
def modify_event(event_name):
    '''
    request:
        path parameter: event_name.
    responses:
        200:
            description: message that event is updated succesfully
        404:
            description: event not found
    '''
    try:
        data = request.json if request.data else None
        if not data or api_ops.validate_event(data) == "invalid":
            raise InvalidEventException
        event = api_ops.update_event(event_name, data.get("description"), data.get("rules"))
        if not event:
            return jsonify(error='Event not found'), HTTPStatus.NOT_FOUND
        
        return jsonify(message='Event updated successfully'), HTTPStatus.OK
    
    except InvalidEventException as e:
        return jsonify(message =e.description), e.code
    except:
        return jsonify(message ="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR
