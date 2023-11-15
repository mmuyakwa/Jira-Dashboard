from flask import Flask, render_template
import os
from dotenv import load_dotenv
from jira import JIRA
from threading import Thread
import time
from datetime import datetime

def get_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')
    formatted_date = date_object.strftime('%Y-%m-%d %H:%M')
    return formatted_date

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize JiraClient with credentials
jira_options = {'server': os.getenv('JIRA_SERVER')}
jira_client = JIRA(options=jira_options, basic_auth=(os.getenv('EMAIL'), os.getenv('JIRA_TOKEN')))

# Data structure to store ticket information
tickets_data = {}

# Interval for updating tickets (in seconds)
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 300))

def update_tickets():
    global tickets_data
    while True:
        # Get tickets for each team member
        with open('team.txt', 'r') as file:
            team_members = [line.strip() for line in file.readlines()]

        # Update tickets for each team member
        for member in team_members:
            issues = jira_client.search_issues(f'assignee = \"{member}\" ORDER BY updated DESC')
            tickets_data[member] = [
                {
                    'url': issue.permalink(),
                    'email': member,
                    'title': issue.fields.summary,
                    'priority': issue.fields.priority.name,
                    'assigned_date': get_date(issue.fields.created), #'assigned_date': issue.fields.created
                    'updated_date': get_date(issue.fields.updated) #'updated_date': issue.fields.updated
                }
                for issue in issues
            ]
        time.sleep(UPDATE_INTERVAL)

# Start the background thread for updating tickets
update_thread = Thread(target=update_tickets)
update_thread.daemon = True
update_thread.start()

@app.route('/')
def index():    
    # Sort tickets by date of assignment (newest first)
    sorted_tickets = sorted(
         [(member, tickets) for member, tickets_list in tickets_data.items() for tickets in tickets_list],
         key=lambda item: item[1]['updated_date'],
         reverse=True
    ) if tickets_data else []
    
    
    return render_template('index.html', tickets=sorted_tickets)

if __name__ == '__main__':
    app.run(debug=True)
