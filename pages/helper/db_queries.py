import os
import sqlite3
from sqlmodel import create_engine, Session, select, SQLModel
from sqlalchemy import or_
from pages.helper.data_models import RegisteredCases, PublicSubmissions

# --- Absolute DB path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlite_url = f"sqlite:///{os.path.join(BASE_DIR, 'sqlite_database.db')}"
engine = create_engine(sqlite_url)


def create_db():
    """Create the database tables if not exist."""
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"[DB] Error creating tables: {e}")


# ----------------------- CASE REGISTRATION -----------------------

def register_new_case(case_details: RegisteredCases) -> str:
    with Session(engine) as session:
        session.add(case_details)
        session.commit()
        session.refresh(case_details)
        return case_details.id


def fetch_registered_cases(submitted_by: str, status: str):
    """Fetch registered cases filtered by submitter and status."""
    if status == "All":
        status = ["F", "NF"]
    elif status == "Found":
        status = ["F"]
    elif status == "Not Found":
        status = ["NF"]

    with Session(engine) as session:
        result = session.exec(
            select(
                RegisteredCases.id,
                RegisteredCases.name,
                RegisteredCases.age,
                RegisteredCases.status,
                RegisteredCases.last_seen,
                RegisteredCases.matched_with,
            )
            .where(
                or_(
                    RegisteredCases.submitted_by == submitted_by,
                    RegisteredCases.submitted_by.ilike(f"%{submitted_by}%")
                )
            )
            .where(RegisteredCases.status.in_(status))
        ).all()
        return result


def get_not_confirmed_registered_cases(submitted_by: str):
    with Session(engine) as session:
        return session.query(RegisteredCases).filter(
            RegisteredCases.submitted_by == submitted_by
        ).all()


def get_training_data(submitted_by: str):
    with Session(engine) as session:
        return session.exec(
            select(RegisteredCases.id, RegisteredCases.face_mesh)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == "NF")
        ).all()


# ----------------------- PUBLIC CASE HANDLING -----------------------

def new_public_case(public_case_details: PublicSubmissions):
    with Session(engine) as session:
        session.add(public_case_details)
        session.commit()


def fetch_public_cases(train_data: bool, status: str):
    if train_data:
        with Session(engine) as session:
            return session.exec(
                select(PublicSubmissions.id, PublicSubmissions.face_mesh)
                .where(PublicSubmissions.status == status)
            ).all()

    with Session(engine) as session:
        return session.exec(
            select(
                PublicSubmissions.id,
                PublicSubmissions.status,
                PublicSubmissions.location,
                PublicSubmissions.mobile,
                PublicSubmissions.birth_marks,
                PublicSubmissions.submitted_on,
                PublicSubmissions.submitted_by,
            )
            .where(PublicSubmissions.status == status)
        ).all()


def get_public_case_detail(case_id: str):
    with Session(engine) as session:
        return session.exec(
            select(
                PublicSubmissions.location,
                PublicSubmissions.submitted_by,
                PublicSubmissions.mobile,
                PublicSubmissions.birth_marks,
            ).where(PublicSubmissions.id == case_id)
        ).all()


def get_registered_case_detail(case_id: str):
    with Session(engine) as session:
        return session.exec(
            select(
                RegisteredCases.name,
                RegisteredCases.complainant_mobile,
                RegisteredCases.age,
                RegisteredCases.last_seen,
                RegisteredCases.birth_marks,
            ).where(RegisteredCases.id == case_id)
        ).all()


def list_public_cases():
    with Session(engine) as session:
        return session.exec(select(PublicSubmissions)).all()


# ----------------------- STATUS & MATCHING -----------------------

def update_found_status(register_case_id: str, public_case_id: str):
    with Session(engine) as session:
        registered_case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == str(register_case_id))
        ).one()
        registered_case.status = "F"
        registered_case.matched_with = str(public_case_id)

        public_case = session.exec(
            select(PublicSubmissions).where(PublicSubmissions.id == str(public_case_id))
        ).one()
        public_case.status = "F"

        session.commit()


def get_registered_cases_count(submitted_by: str, status: str):
    create_db()
    with Session(engine) as session:
        return session.exec(
            select(RegisteredCases)
            .where(RegisteredCases.submitted_by == submitted_by)
            .where(RegisteredCases.status == status)
        ).all()


# ----------------------- GENAI EXTRA COLUMNS -----------------------

def save_alert(case_id: str, alert_text: str):
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        case.alert_draft = alert_text
        session.commit()


def save_match_explanation(case_id: str, explanation_text: str):
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        case.match_explanation = explanation_text
        session.commit()


def save_lead_priority(case_id: str, priority_info: str):
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        case.lead_priority = priority_info
        session.commit()


def save_witness_summary(case_id: str, witness_summary: str):
    with Session(engine) as session:
        case = session.exec(
            select(RegisteredCases).where(RegisteredCases.id == case_id)
        ).one()
        case.witness_summary = witness_summary
        session.commit()


if __name__ == "__main__":
    create_db()
    print("[DB] Tables ready.")
