'''
 models.py
 
 This file contains the basic data model for an Event
'''

from dataclasses import dataclass

@dataclass
class Event:
    name: str
    startDate: str
    endDate: str
    location: str
    link: str