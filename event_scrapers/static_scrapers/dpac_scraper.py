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
            date = event.select_one('.date')['aria-label']
            print(date)
            location = "DPAC - Durham, NC"
            link = event.select_one('a')['href']

            events.append(
                Event(
                    name=name,
                    date=date,
                    location=location,
                    link=link
                )
            )
        except Exception as e:
            print(f"Skipping malformed event: {e}")
            continue
    return events