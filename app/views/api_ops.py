from models.db_mock import TRACKING_PLAN, EVENTS, EVENT_TRACKING_MAP

def set_event_tracking_mapping(tracking_plan_id, event):
    '''
        Association table writing
    '''
    if EVENT_TRACKING_MAP.get(event["name"]):
        if not tracking_plan_id in EVENT_TRACKING_MAP[event["name"]]:
            EVENT_TRACKING_MAP[event["name"]].append(tracking_plan_id)  
    else:
        EVENT_TRACKING_MAP[event["name"]] = [tracking_plan_id] 
    print(f'{TRACKING_PLAN = }\n {EVENTS = }\n {EVENT_TRACKING_MAP = }\n')

def set_tracking_plan(display_name, description, events_data):
    '''
        Generate id for tracking plan and insert into db
    '''
    tracking_plan_id = max(TRACKING_PLAN, key= lambda x: x) + 1 if TRACKING_PLAN else 1
    TRACKING_PLAN[tracking_plan_id] = {"display_name": display_name, "description": description, "events": [event["name"] for event in events_data]}
    return tracking_plan_id


def set_event(event):
    '''
        Create and Insert event into db
    '''
    EVENTS[event["name"]] = {"name": event["name"], "description": event["description"], "rules": event["rules"]}
    return event["name"]


def validate_event(event):
    '''
        Validate event data if event already exists in db
    '''
    if EVENTS.get(event["name"]):
        if event != EVENTS[event["name"]]:
            return "error"
        return "exists"
    return "clear"

def get_event(event_name):
    '''
        get the event from db
    '''
    event = EVENTS.get(event_name)
    if not event:
        return None
    else:
        return event

def update_event(event_name, description, rules):
    '''
        update the event in db
    '''
    event = EVENTS.get(event_name)
    if not event:
        return None
    event["description"] = description
    event["rules"] = rules
    return event

def get_tracking_plan(tracking_plan_name):
    '''
        Fetch all the tracking plans with tracking plan name
        attach all the events of each fetched tracking plan together
    '''
    tracking_plan = {"display_name": "", "description": "", "events": []}
    for id in TRACKING_PLAN:
        if TRACKING_PLAN[id]["display_name"] == tracking_plan_name:
            tracking_plan["display_name"] = tracking_plan_name
            tracking_plan["description"] = TRACKING_PLAN[id]["description"]
            if tracking_plan.get("events") :
                tracking_plan["events"].extend([EVENTS[event] for event in TRACKING_PLAN[id]["events"]])
            else:
                tracking_plan["events"] = [EVENTS[event] for event in TRACKING_PLAN[id]["events"]]
    if tracking_plan["events"]:
        tracking_plan["events"] = list(set(tracking_plan["events"]))
    if not tracking_plan["display_name"]:
        return {}
    return tracking_plan

def get_tracking_plans():
    all_tracking_plans = []
    for id in TRACKING_PLAN:
        all_tracking_plans.append({
            "display_name": TRACKING_PLAN[id].get("display_name"),
            "description": TRACKING_PLAN[id].get("description"),
            "events": [EVENTS[event] for event in TRACKING_PLAN[id]["events"]]
        })
    return all_tracking_plans

def update_tracking_plan(tracking_plan_name, display_name, events):
    '''
        Get all the tracking plans with name tracking_plan_name and update the values
        create new events if updated tracking plan has new events
        Update the EVENT_TRACKING_MAP associate table
    '''
    previous_events = []
    is_plan_present = False
    is_create_event = False
    for event in events:
        if not EVENTS[event["name"]]:
            set_event(event)
    for id in TRACKING_PLAN:
        if TRACKING_PLAN[id]["display_name"] == tracking_plan_name:
            is_plan_present = True
            previous_events = TRACKING_PLAN[id]["events"]

            TRACKING_PLAN[id]["display_name"] = display_name
            TRACKING_PLAN[id]["events"] = [event["name"] for event in events]

            for event in previous_events:
                if id in EVENT_TRACKING_MAP[event]:
                    EVENT_TRACKING_MAP[event].remove(id)   # detach tracking plan from previous events

            for event in events:
                if not is_create_event:
                    set_event(event)
                    is_create_event = True
                if id not in EVENT_TRACKING_MAP[event["name"]]:
                    EVENT_TRACKING_MAP[event["name"]].append(id)    # attach tracking plan to even

    return is_plan_present