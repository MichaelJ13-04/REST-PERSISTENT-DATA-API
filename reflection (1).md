# Reflection: REST Persistent Data API

For this assignment, I created a Flask REST API that accepts clinical patient records and stores them in both a SQLite database and a JSON Lines file. I first set up the Python environment and installed Flask, SQLAlchemy, and Pydantic. Then I created the ClinicalData database model, added three patient-data fields—age, blood pressure, and heart rate, along with temperature—and used a Pydantic schema to validate incoming information. I built a POST endpoint to save records and a GET endpoint to retrieve them.

One thing that stood out to me was that the same record can be represented in two storage formats for different purposes. As the code evolved, I connected validation, database persistence, and JSONL logging into one workflow. I now better understand how APIs, schemas, and persistent storage work together. I would like to learn more about handling failures across multiple storage systems so both copies always remain consistent.
