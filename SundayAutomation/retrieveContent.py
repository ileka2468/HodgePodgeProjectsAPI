import datetime
import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database import Service
from sqlalchemy import and_
from makePPTX import PowerPointmaker
from UploadPPTX import StartUpload
import calendar
import chromedriver_autoinstaller
from dotenv import load_dotenv
load_dotenv()


def getCalendars(driver):
    month_bank = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
    body = driver.find_element(By.CLASS_NAME, "lessonPageMargins")
    calendar_center = body.find_elements(By.XPATH, "*")[-1]
    calendars = calendar_center.find_elements(By.TAG_NAME, 'table')
    calendar_only_element_list = {}

    for calendar in calendars:
        try:
            tbody = calendar.find_element(By.TAG_NAME, 'tbody')
            month_heading = \
                tbody.find_element(By.TAG_NAME, 'tr').find_element(By.TAG_NAME, 'td').text.strip().split(" ")[0]
            if month_heading in month_bank:
                calendar_only_element_list[f"{month_heading}"] = tbody

        except NoSuchElementException:
            pass
    return calendar_only_element_list


def getDatabaseDates():
    engine = create_engine(os.environ.get('EMAIL_DB'), pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    session = Session()

    target_month = datetime.datetime.now().month
    target_year = datetime.datetime.now().year
    target_month = 7

    dates_list = []

    days_in_month = calendar.monthrange(int(target_year), int(target_month))
    start_date = f"{target_year}-{target_month}-1"
    end_date = f"{target_year}-{target_month}-{days_in_month[1]}"

    results = session.query(Service).filter(and_(Service.date >= start_date, Service.date <= end_date, Service.status == 0)).all()
    print(results)

    if len(results) == 0:
        return "All Content already done for this month"

    for date in results:
        dates_list.append(str(date)[str(date).find(" ") + 1:])

    return dates_list


def getFirstReading(driver, article):
    return article.find_element(By.TAG_NAME, 'div').text


def getPsalm(driver, article):
    return article.find_element(By.TAG_NAME, 'div').text


def getSecondReading(driver, article):
    return article.find_element(By.TAG_NAME, 'div').text


def getGospel(driver, article):
    return article.find_element(By.TAG_NAME, 'div').text


def grabContent(date, calendars, driver):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')

    month = date.strftime("%B")
    target_day = date.day

    target_calendar = calendars[month]

    table_rows = target_calendar.find_elements(By.TAG_NAME, 'tr')

    for row in table_rows:
        row_days = row.find_elements(By.TAG_NAME, 'td')
        for td in row_days:
            try:
                day = td.find_element(By.TAG_NAME, 'font').text.strip()

                if day and day == str(target_day):
                    print("FOUND CORRECT DATE!")
                    td.find_element(By.TAG_NAME, 'a').click()

                    article_list = driver.find_element(By.CLASS_NAME, 'lessonPageMargins').find_elements(By.TAG_NAME,
                                                                                                         'article')
                    article_dict = {}

                    for article in article_list:
                        if "Old Testament" in article.text:
                            # checking to see if key exists, first occurence found should trigger error and populate
                            if article_dict.get("first_reading") is None:
                                article_dict["first_reading"] = article
                            else:
                                print("detected duplicate first reading, using first occurence")

                        elif "Psalm" in article.text:
                            if article_dict.get("psalm") is None:
                                article_dict["psalm"] = article
                            else:
                                print("detected duplicate psalm, using first occurence")

                        elif "The Epistle" in article.text:
                            if article_dict.get("second_reading") is None:
                                article_dict["second_reading"] = article
                            else:
                                print("detected duplicate second reading, using first occurence")

                        elif "The Gospel" in article.text:
                            if article_dict.get("gospel") is None:
                                article_dict["gospel"] = article
                            else:
                                print("detected duplicate first reading, using first occurence")

                    first_reading = getFirstReading(driver, article_dict["first_reading"])

                    psalm = getPsalm(driver, article_dict["psalm"])

                    second_reading = getSecondReading(driver, article_dict["second_reading"])

                    gospel = getGospel(driver, article_dict["gospel"])

                    return_data = {
                        "first_reading": first_reading,
                        "psalm": psalm,
                        "second_reading": second_reading,
                        "gospel": gospel
                    }

                    ppmkr = PowerPointmaker(return_data, str(date).split(" ")[0])

                    driver.back()

            except NoSuchElementException:
                pass



def getReadings():
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.get("https://lectionarypage.net/")

    '''
    Using the current date will be temporary as production code will query the database for all the sundays in the
    current month.
    '''

    target_dates = getDatabaseDates()
    if target_dates == "All Content already done for this month":
        return "All Content already done for this month"
    else:
        calendars = getCalendars(driver)

        for date in target_dates:
            grabContent(date, calendars, driver)


def main2():
    dates = getReadings()
    if dates == "All Content already done for this month":
        print("No dates to fufill currently")
        return
    print("Starting File Upload")
    StartUpload()


if __name__ == '__main__':
    main2()
