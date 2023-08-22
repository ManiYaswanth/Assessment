# Tracking Plan Management System

# Introduction 
This project is a Tracking Plan Management System built using Python and Flask. It allows you to manage tracking plans and associated events for your application.

## Overview
The Tracking Plan Management System is designed to help you create, update, and manage tracking plans and events for your application. It provides API endpoints and User Interface to interact with the system and perform various actions related to tracking plans and events.

## Features
- Create and manage tracking plans with display name and description.
- Define events with name, description, and associated rules.
- Associate tracking plans with events and vice versa.
- Retrieve tracking plans and their associated events.
- Update tracking plans and events.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following installed:

- Python
- Flask
- A database system (SQLite, PostgreSQL, etc.)

### Installation

1. Clone this repository:

```bash
git clone https://github.com/ManiYaswanth/Assessment.git
```

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

3. Navigate to the project directory:

```bash
cd app/
```
Configure the database connection in /models/db_config.py.

4. Run the application:

```bash
flask --app main run
```
The application will be accessible at http://localhost:5000

## Usage
Use API endpoints to manage tracking plans and events.
Create, update, and retrieve tracking plans and events.
Associate tracking plans with events for effective tracking.

## Database Structure
The database structure includes tables for tracking plans, events, and event-tracking plan associations.

## API Endpoints
- POST /tracking_plans - Create a new tracking plan.
- GET /tracking_plans - Get a list of all tracking plans.
- GET /tracking_plans/<tracking_plan_name> - Get details of a specific tracking plan.
- PUT /tracking_plans/<tracking_plan_name> - Update a tracking plan.
- POST /events - Create a new event.
- GET /event/<event_name> - Get details of a specific event
- PUT /events/<event_name> - Update an event.

payload for "/tracking_plan" endpoints - 
```JSON
{ 
	"tracking_plan": {
        "display_name": "Tracking Plan name",
        "rules": {
            "events": [
                {
                    "name": "event name",
                    "description": "event description",
                    "rules": {
                        { JSON SCHEMA }
                }
              }
            ]
        }
    }
}
```

payload for "/event" endpoints - 
```JSON 
{
    "name": "Event name",
    "description": "Event description",
    "rules": {
        { JSON SCHEMA }
    }
}
```
## Note
db table definitions is written in app/models/db_models.py which is never used, instead a mimic of db is created using python data structures and stored in memory while the application runs - refer app/models/db_mock.py

## Contribute
Contributions are welcome! Feel free to open issues and pull requests.