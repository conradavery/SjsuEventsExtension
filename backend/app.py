from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/events', methods=['GET'])
def get_today_events():
    try:
        # Step 1: Send a request to the webpage
        url = "https://events.sjsu.edu"  # Replace with the actual URL of the events page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        events_dict = {}

        # Step 2: Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Step 3: Find all event cards
        event_cards = soup.find_all('div', class_='em-card')

        # Step 4: Loop through each event card and extract details
        today_date = datetime.now().strftime("%a, %b %d, %Y")
        # print(f"Today's Date: {today_date}")  # Debugging

        events = []

        for card in event_cards:
            # Extract event title
            title_tag = card.find('h3', class_='em-card_title')
            title = title_tag.text.strip() if title_tag else "No Title"

            # Extract event link as unique identifier
            if title_tag and title_tag.find('a') and title_tag.find('a').has_attr('href'):
                event_link = title_tag.find('a')['href']
                # Make sure the link is absolute
                if not event_link.startswith('http'):
                    event_link = f"https://events.sjsu.edu{event_link}"  # Adjust base URL as needed
            else:
                event_link = "No Link"

            # Check for duplicates
            if event_link in events_dict:
                # print(f"Duplicate event found: {event_link} - Skipping.")
                continue  # Skip duplicate
            events_dict[event_link] = {
                'title': title,
                'link': event_link
            }

            # Extract event date
            date_tag = card.find('p', class_='em-card_event-text')
            date_str = date_tag.text.strip() if date_tag else "No Date"
            # Attempt to parse the date string into a datetime object
            try:
                # Adjust the format string based on the actual date format on the website
                # Example format: "Wed, Sep 27, 2024"
                sort_date = date_str.split(" ", 4)[:4]
                formatted_date = " ".join(sort_date)
            except ValueError:
                # Handle cases where the date format doesn't match
                print(f"Date parsing failed for event: {title}, Date string: {date_str}")
                formatted_date = "Invalid Date"

            # Debugging
            # print(f"Event: {title}")
            # print(f"Formatted Event Date: {formatted_date}")

            # Extract location
            location_tag = date_tag.find_next('p', class_='em-card_event-text') if date_tag else None
            location = location_tag.text.strip() if location_tag else "No Location"

            # Extract event category (tag)
            category_tag = card.find('div', class_='em-list_tags')
            category = category_tag.text.strip() if category_tag else "No Category"

            # Only include events happening today
            if formatted_date == today_date:
                events.append({
                    'title': title,
                    'date': date_str,
                    'category': category,
                    'link': event_link,
                    'location': location
                })
                # # Print the extracted details
                # print(f"Event Title: {title}")
                # print(f"Event Date: {date_str}")
                # print(f"Event Category: {category}")
                # print(f"Event Link: {event_link}")
                # print(f"Event Location: {location}\n")

        return jsonify({'status': 'success', 'events': events}), 200

    except Exception as e:
        print(f"Error occurred: {e}")  # Debugging
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    pass

if __name__ == '__main__':
    # For development purposes, use debug=True. In production, set debug=False
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
