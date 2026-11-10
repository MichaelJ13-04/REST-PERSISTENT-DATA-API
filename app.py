from pathlib import Path
import json
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import create_engine, Integer, String, Float, DateTime, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


# Keep the database and JSONL file beside this Python file.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = BASE_DIR / "clinical_data.db"
JSONL_PATH = DATA_DIR / "clinical_data.jsonl"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    echo=False
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# SQLAlchemy database model
class ClinicalData(Base):
    __tablename__ = "clinical_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    diagnosis: Mapped[str] = mapped_column(String(250), nullable=False)

    # Three additional clinical patient-data columns
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    blood_pressure: Mapped[str] = mapped_column(String(20), nullable=False)
    heart_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


# Pydantic schema validates incoming patient data
class ClinicalDataCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    patient_name: str = Field(min_length=1, max_length=100)
    diagnosis: str = Field(min_length=1, max_length=250)
    age: int = Field(ge=0, le=120)
    blood_pressure: str = Field(min_length=3, max_length=20)
    heart_rate: int = Field(gt=0, le=300)
    temperature_c: float = Field(gt=25, lt=45)


app = Flask(__name__)

# Create the SQLite table if it does not already exist.
Base.metadata.create_all(engine)


def record_to_dict(record: ClinicalData) -> dict:
    """Convert a database record into JSON-serializable data."""
    return {
        "id": record.id,
        "patient_name": record.patient_name,
        "diagnosis": record.diagnosis,
        "age": record.age,
        "blood_pressure": record.blood_pressure,
        "heart_rate": record.heart_rate,
        "temperature_c": record.temperature_c,
        "created_at": record.created_at.isoformat()
    }


@app.route("/clinical/", methods=["POST"])
def create_clinical_record():
    try:
        payload = ClinicalDataCreate.model_validate(request.get_json(silent=True) or {})
    except ValidationError as error:
        return jsonify({
            "error": "Validation failed",
            "details": error.errors()
        }), 400

    new_record = ClinicalData(**payload.model_dump())

    # First persist the record in SQLite.
    try:
        with SessionLocal() as session:
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            saved_record = record_to_dict(new_record)

        # Then append the same record as one JSON object per line.
        with JSONL_PATH.open("a", encoding="utf-8") as jsonl_file:
            jsonl_file.write(json.dumps(saved_record) + "\n")

    except Exception as error:
        app.logger.exception("Could not save the clinical record")
        return jsonify({
            "error": "Could not save the clinical record",
            "details": str(error)
        }), 500

    return jsonify({
        "message": "Clinical record created successfully",
        "record": saved_record
    }), 201


@app.route("/clinical/", methods=["GET"])
def get_clinical_records():
    with SessionLocal() as session:
        records = session.scalars(
            select(ClinicalData).order_by(ClinicalData.id)
        ).all()

        return jsonify([record_to_dict(record) for record in records]), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Clinical Records REST API",
        "endpoints": {
            "create_record": "POST /clinical/",
            "list_records": "GET /clinical/"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
