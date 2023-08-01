from datetime import date, timedelta

from imagekitio.models.CreateFolderRequestOptions import CreateFolderRequestOptions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Service
from imagekitio import ImageKit
import os
import dotenv
dotenv.load_dotenv()

imagekit = ImageKit(
    public_key=os.environ.get("IMAGEKIT_PUBLIC_KEY"),
    private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY"),
    url_endpoint='https://ik.imagekit.io/smec/'
)


def allsundays(year):
    d = date(year, 1, 1)  # January 1st
    d += timedelta(days=6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days=7)


def main():
    engine = create_engine(os.environ.get('EMAIL_DB'), pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    session = Session()
    

if __name__ == '__main__':
    main()
