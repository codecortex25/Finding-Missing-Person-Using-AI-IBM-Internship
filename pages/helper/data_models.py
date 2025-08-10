from uuid import uuid4
from datetime import datetime
from sqlmodel import Field, create_engine, SQLModel


class PublicSubmissions(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid4()), nullable=False
    )
    submitted_by: str = Field(max_length=128, nullable=True)
    face_mesh: str = Field(nullable=False)  # JSON string of face mesh landmarks
    location: str = Field(max_length=128, nullable=True)
    mobile: str = Field(max_length=10, nullable=False)
    email: str = Field(max_length=64, nullable=True)
    status: str = Field(max_length=16, nullable=False)  # e.g., "F", "NF"
    birth_marks: str = Field(max_length=512, nullable=True)
    submitted_on: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class RegisteredCases(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: str = Field(
        primary_key=True, default_factory=lambda: str(uuid4()), nullable=False
    )
    submitted_by: str = Field(max_length=64, nullable=False)
    name: str = Field(max_length=128, nullable=False)
    father_name: str = Field(max_length=128, nullable=True)
    age: str = Field(max_length=8, nullable=True)
    complainant_name: str = Field(max_length=128, nullable=False)
    complainant_mobile: str = Field(max_length=10, nullable=True)
    adhaar_card: str = Field(max_length=12, nullable=True)
    last_seen: str = Field(max_length=64, nullable=True)
    address: str = Field(max_length=512, nullable=True)
    face_mesh: str = Field(nullable=False)  # JSON string of face mesh landmarks
    submitted_on: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    status: str = Field(max_length=16, nullable=False)  # "F" = Found, "NF" = Not Found
    birth_marks: str = Field(max_length=512, nullable=True)
    matched_with: str = Field(nullable=True)

    # ----------------- GENAI INTEGRATION FIELDS -----------------
    alert_draft: str = Field(nullable=True)            # AI-generated public alert
    match_explanation: str = Field(nullable=True)      # AI explanation for match
    lead_priority: str = Field(nullable=True)          # AI ranking of leads
    witness_summary: str = Field(nullable=True)        # AI witness statement summary


if __name__ == "__main__":
    sqlite_url = "sqlite:///sqlite_database.db"
    engine = create_engine(sqlite_url)

    # Create tables if not exist
    SQLModel.metadata.create_all(engine)
    print("[DB] Tables created or already exist.")
