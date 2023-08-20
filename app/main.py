from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from api import (
    api
)
app = Flask(__name__)

app.register_blueprint(api.mod, url_prefix="/")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mani123@localhost:5432/demo_project'

db = SQLAlchemy(app)

class TrackingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(255), nullable=False)
    events = db.relationship('Event', secondary='tracking_plan_event', back_populates='tracking_plans')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    rules = db.Column(db.JSON, nullable=False)
    tracking_plans = db.relationship('TrackingPlan', secondary='tracking_plan_event', back_populates='events')

tracking_plan_event = db.Table('tracking_plan_event',
    db.Column('tracking_plan_id', db.Integer, db.ForeignKey('tracking_plan.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



if __name__ == '__main__':
    app.run(debug=True)
