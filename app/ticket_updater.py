import time
from threading import Thread
from app import get_team_tickets

# Interval in seconds
UPDATE_INTERVAL = 300

def update_tickets():
    while True:
        # Hier wird die Funktion get_team_tickets aufgerufen, um die Tickets zu aktualisieren.
        # Die aktualisierten Ticketdaten sollten in einer geeigneten Datenstruktur gespeichert werden.
        # Beispiel: ticket_data = get_team_tickets('team.txt')
        # Diese Datenstruktur wird dann von der Flask-Anwendung verwendet.
        time.sleep(UPDATE_INTERVAL)

# Start the background thread
update_thread = Thread(target=update_tickets)
update_thread.start()
