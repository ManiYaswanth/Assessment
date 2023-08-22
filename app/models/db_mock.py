'''
    This is a mimic for db structure. This is created to exempt the hosting of db server and also free from using other python libraries.
'''

TRACKING_PLAN = {}
# {"display_name": {"display_name": "name", "description": "", "event": "eventA"}, {..}}
# {"id": {"display_name": "", events: []}}

EVENTS = {}
#{"event_name": {}}


EVENT_TRACKING_MAP = {}
#{"event_name": [tracking_ids]}
