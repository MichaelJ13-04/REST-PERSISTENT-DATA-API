# REST Persistent Data API

## Project Overview

This project is a Flask-based REST API designed to store and retrieve clinical patient data using two forms of persistent storage: SQLite and JSON Lines (JSONL).

The API uses SQLAlchemy to manage database records and Pydantic to validate incoming patient information before it is saved.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- Pydantic
- JSON Lines (JSONL)

## Clinical Data Fields

The API collects the following information:

- Patient Name
- Diagnosis
- Age
- Blood Pressure
- Heart Rate
- Temperature (Celsius)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Displays API information |
| POST | `/clinical/` | Creates and stores a clinical record |
| GET | `/clinical/` | Retrieves saved clinical records |

## Data Storage

The project uses two storage formats:

1. **SQLite Database:** Stores clinical records in `clinical_data.db`.
2. **JSON Lines File:** Stores each clinical record as a separate JSON object in `data/clinical_data.jsonl`.

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in Visual Studio Code.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Flask application:

```bash
python app.py
```

5. Open the API at:

```text
http://127.0.0.1:5000/
```

## Testing the API

To create a clinical record, send a POST request to:

```text
http://127.0.0.1:5000/clinical/
```

Example JSON request:

```json
{
  "patient_name": "John Smith",
  "diagnosis": "Hypertension",
  "age": 45,
  "blood_pressure": "130/85",
  "heart_rate": 78,
  "temperature_c": 37.0
}
```

To retrieve saved records, send a GET request to:

```text
http://127.0.0.1:5000/clinical/
```

## Validation

Pydantic validates incoming clinical data to help ensure that required fields contain acceptable values. Invalid submissions return a validation error instead of being stored.

## Project Purpose

The purpose of this assignment was to demonstrate how REST APIs can work with persistent data storage. By combining SQLite and JSON Lines, the project demonstrates database management, data validation, and record logging.

