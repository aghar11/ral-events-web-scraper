'''
 dpac_scraper.py

 This file contains the functionality for event information retrieval from the Durham Performing Arts Center website.
'''

import requests
from bs4 import BeautifulSoup
from event_scrapers.models import Event
from urllib.parse import urljoin

BASE_URL = "https://www.dpacnc.com"
EVENTS_URL = f"{BASE_URL}/events/all"

def get_dpac_events():
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
                endDate = ""
            else:
                startDate = event.select_one('.m-date__rangeFirst').get_text()
                endDate = event.select_one('.m-date__rangeLast').get_text()
            location = "DPAC - Durham, NC"
            link = event.select_one('a')['href']

            events.append(
                Event(
                    name=name,
                    startDate=startDate,
                    endDate=endDate,
                    location=location,
                    link=link
                )
            )
        except Exception as e:
            print(f"Skipping malformed event: {e}")
            continue
    return events