import caldav
from datetime import datetime, timedelta
from caldav.elements import dav, cdav

# Apple Calendar CalDAV URL
CALDAV_URL = "https://caldav.icloud.com/"
USERNAME = "scythe213@gmail.com"
PASSWORD = "lvmy-ghms-qsyk-dmrk"

# Connect to Apple Calendar via CalDAV
client = caldav.DAVClient(url=CALDAV_URL, username=USERNAME, password=PASSWORD)
principal = client.principal()

# Get all calendars
calendars = principal.calendars()

if not calendars:
    print("No calendars found!")
    exit()

# Select the first calendar (modify as needed)
calendar = calendars[0]

# Define the date range (past 7 days)
end_date = datetime.today()
start_date = end_date - timedelta(days=3)

# Fetch events
events = calendar.search(start=start_date, end=end_date)

# Print event details
for event in events:
    ics_data = event.data  # Raw .ics data
    vevent = event.vobject_instance.vevent
    uid = vevent.uid.value  # Stable UID
    summary = vevent.summary.value
    start_time = vevent.dtstart.value
    end_time = vevent.dtend.value
    
    print(f"Event UID: {uid}")
    print(f"Event: {summary}")
    print(f"Start: {start_time}")
    print(f"End: {end_time}")
    print("-" * 40)