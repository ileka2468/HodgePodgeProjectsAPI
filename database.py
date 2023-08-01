from sqlalchemy import Column, String, BINARY, INT, DATE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class License(Base):
    __tablename__ = "KeyInfo"

    key = Column("key", BINARY(100), primary_key=True)
    mid = Column("mid", String(100))

    def __init__(self, key, mid=None):
        self.key = key
        self.mid = mid

    def __repr__(self):
        return f"License Hash: {self.key}, Machine ID: {self.mid}"


class Emails(Base):
    __tablename__ = "smec_email"

    email_id = Column("email_id", INT, primary_key=True, autoincrement=True)
    email = Column("email", String(200), nullable=False)

    def __init__(self, email):
        self.email = email
    def __repr__(self):
        return f"Email: {self.email}"


class Service(Base):
    __tablename__ = "service_dates"

    date_id = Column("date_id", INT, primary_key=True, autoincrement=True)
    date = Column("date", DATE, nullable=False)

    def __init__(self, date):
        self.date = date
    def __repr__(self):
        return f"Date: {self.date}"
