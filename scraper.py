from event_scrapers.static_scrapers.dpac_scraper import get_dpac_events

def main():
    events = get_dpac_events()
    for event in events:
        if event.endDate != "":
            print(f"{event.startDate} to {event.endDate} - {event.name} @ {event.location}")
        else:
            print(f"{event.startDate} - {event.name} @ {event.location}")
        print(f"More info: {event.link}\n")

if __name__ == "__main__":
    main()