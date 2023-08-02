import datetime
import os
import dotenv
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Service

dotenv.load_dotenv()


def StartUpload():
    grabFile()
    clearFolders()
    print("Upload Finished, and Folders Cleared!")


def upload(file_list, tag):
    engine = create_engine(os.environ.get('EMAIL_DB'), pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    session = Session()

    for file in file_list:
        foldername = file[file.find("-") + 1: file.find(".")].strip()
        imagekit = ImageKit(
            public_key=os.environ.get("IMAGEKIT_PUBLIC_KEY"),
            private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY"),
            url_endpoint=f'https://ik.imagekit.io/smec'
        )

        print(f"{tag}/{file}")

        up = imagekit.upload(
            file=open(f"{tag}/{file}", "rb"),
            file_name=f"{file}",
            options=UploadFileRequestOptions(
                tags=[f"{tag}"],
                use_unique_file_name=False,
                folder=f"smec_readings/{foldername}"
            )
        )
        target_date = file[file.find("-") + 1: file.find(".")].strip()
        record_to_update = session.query(Service).filter(Service.date == target_date).first()
        record_to_update.status = 1
        record_to_update.content = up.url
        with open("logs.txt", "a") as logger:
            logger.write(
                f"Filename: {file}\nUpload ID: {up.file_id}\nTime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUpload Status:{up.response_metadata.http_status_code}\n\n")

    session.commit()

def grabFile():
    # probably refactor this an use a loop but tbh who cares...
    first_readings = os.listdir("First Readings")
    upload(first_readings, "First Readings")
    psalms = os.listdir("Psalms")
    upload(psalms, "Psalms")
    second_readings = os.listdir("Second Readings")
    upload(second_readings, "Second Readings")
    gospels = os.listdir("Gospels")
    upload(gospels, "Gospels")


def clearFolders():
    print("Deleting Powerpoints...")
    folder_list = ["First Readings", "Psalms", "Second Readings", "Gospels"]
    for folder in folder_list:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))


if __name__ == '__main__':
    StartUpload()
