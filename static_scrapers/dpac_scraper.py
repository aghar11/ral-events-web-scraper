'''
 dpac_scraper.py

 This file contains the functionality for event information retrieval from the Durham Performing Arts Center website.
'''

import requests
from bs4 import BeautifulSoup
from db.models import Event
from db.db_config import SessionLocal
from db.models import Event
from dateutil import parser
from datetime import datetime

BASE_URL = "https://www.dpacnc.com"
EVENTS_URL = f"{BASE_URL}/events/all"

## Helper Funtions
def add_event_to_db(event):
    session = SessionLocal()
    try:
        session.add(event)
        session.commit()
    except Exception as e:
        print("Error inserting event:", e)
        session.rollback()
    finally:
        session.close()

def parse_date(date_str, default_year=None):
    try:
        # Parse using dateutil
        dt = parser.parse(date_str, fuzzy=True)

        return dt
    except Exception as e:
        print(f"Error parsing date: {date_str} -> {e}")
        return None

## Main function
def save_dpac_events():
    res = requests.get(EVENTS_URL)
    
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    event_elements = soup.select('.eventItem')

    events = []
    for event in event_elements:
        try:
            name = event.select_one('.title').get_text(strip=True)

            if event.select_one('.m-date__singleDate') is not None:
                startDate = event.select_one('.m-date__singleDate').get_text()
            else:
                startDate = event.select_one('.m-date__rangeFirst').get_text()

            if event.select_one('.m-date__rangeLast') is not None:
                endDate = event.select_one('.m-date__rangeLast').get_text()

                if event.select_one('.m-date__rangeFirst').select_one('.m-date__year') is None:
                    startDate += event.select_one('.m-date__rangeLast').select_one('.m-date__year').get_text()
            else:
                endDate = startDate

            location = "DPAC - Durham, NC"
            link = event.select_one('a')['href']

            events.append(
                Event(
                    name=name,
                    startDate=parse_date(startDate),
                    endDate=parse_date(endDate),
                    location=location,
                    url=link
                )
            )

            add_event_to_db(
                Event(
                    name=name,
                    startDate=parse_date(startDate),
                    endDate=parse_date(endDate),
                    location=location,
                    url=link
                )
            )

        except Exception as e:
            print(f"Skipping malformed event: {e}, {name}")
            continue

    return events