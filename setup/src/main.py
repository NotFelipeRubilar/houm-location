from data import PROPERTY_DATA, USER_DATA
from engine import Session, engine
from models import BaseModel, Property, User


def create_users(db: Session) -> None:
    print(f"Creating {len(USER_DATA)} users")
    with db.begin():
        for u in USER_DATA:
            db.add(User(**u))


def create_properties(db: Session) -> None:
    print(f"Creating {len(PROPERTY_DATA)} properties")
    with db.begin():
        for p in PROPERTY_DATA:
            db.add(Property(**p))


def init_db():
    print("Starting setup")
    BaseModel.metadata.create_all(bind=engine)
    session = Session()

    user = session.query(User).first()
    if user is None:
        create_users(session)
    else:
        print("Users already created")

    property = session.query(Property).first()
    if property is None:
        create_properties(session)
    else:
        print("Properties already created")

    print("Setup finished")


if __name__ == "__main__":
    init_db()
