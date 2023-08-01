from sqlalchemy import create_engine, exists, and_
from sqlalchemy.orm import sessionmaker
from database import License, Emails
import bcrypt
import os


class apiUtils:
    def __init__(self):
        engine = create_engine(os.environ.get('CLOAK_DB'), pool_recycle=3600)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.salt = os.environ.get('SALT').encode('utf-8')

    async def verifyUser(self, provided_key, machine_id):
        print(provided_key, machine_id)

        key_hash = bcrypt.hashpw(provided_key.encode(' dutf-8'), self.salt)
        response = self.session.query(exists().where(and_(License.mid == machine_id, License.key == key_hash))).scalar()

        print(f"The response from the database was {response}")
        if response:
            print(f"The response from the database was {response}")
            return "VERIFIED"
        else:
            return "FAILED"


    async def activateUser(self, provided_key, machine_id):

        key_hash = bcrypt.hashpw(provided_key.encode('utf-8'), self.salt)
        response = self.session.query(License).filter(and_(License.mid == None, License.key == key_hash)).first()
        print(f"The response from the database was {response}")
        if response:
            response.mid = machine_id
            self.session.commit()
            return "ACTIVATED"
        else:
            return "FAILED"

    async def registerEmail(self, email):
        engine = create_engine(os.environ.get('EMAIL_DB'), pool_recycle=3600)
        Session = sessionmaker(bind=engine)
        session = Session()
        response = session.query(Emails.email).filter(Emails.email == email).first()
        if response:
            return "Already Registered"
        else:
            new_email = Emails(email)
            session.add(new_email)
            session.commit()
            return "Registered"
        # check if email arleady exists in db, if not register, if it does than error.
