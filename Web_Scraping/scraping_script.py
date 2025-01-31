import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime

event_urls = ["https://www.asapsports.com/show_events.php?event_id=196462&category=11&year=2024&title=WNBA+DRAFT", 
              "https://www.asapsports.com/show_events.php?event_id=202524&category=11&year=2024&title=WNBA+FINALS%3A+MINNESOTA+VS.+NEW+YORK",
              "https://www.asapsports.com/show_events.php?event_id=198609&category=11&year=2024&title=NBA+DRAFT",
              "https://www.asapsports.com/show_events.php?event_id=198318&category=11&year=2024&title=NBA+FINALS%3A+CELTICS+VS.+MAVERICKS"] 
# URLs to ASAP Sports - WNBA Draft, WNBA Finals, NBA Draft, NBA Finals

output_file = "interviews.csv"
csv_headers = ["event", "date", "person", "quote"]

def get_event_date_links(event_url):
    try:
        response = requests.get(event_url)
        soup = BeautifulSoup(response.text, "html.parser")

        event_date_links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "show_event.php" in href and "date=" in href and href.startswith("http"):
                event_date_links.append(href)
    
        return event_date_links
    
    except Exception as e:
        print(f"Error getting event date links from {event_url}: {e}")
        return []

def get_interview_links(event_url):
    try:
        response = requests.get(event_url)
        soup = BeautifulSoup(response.text, "html.parser")

        interview_links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "show_interview.php" in link["href"]:
                full_url = f"https://www.asapsports.com/{href}" if not href.startswith("http") else href
                interview_links.append(full_url)
        
        return interview_links
    
    except Exception as e:
        print(f"Error getting interview links from {event_url}: {e}")
        return []

def clean_text(text):
    text = " ".join(text.split())
    text = re.sub(r'\s*Q\.\s*', '', text)
    return text.strip()

def scrape_interview(interview_url):
    try:
        response = requests.get(interview_url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title")
        event_name = title.text.strip() if title else "Unknown Event"

        paragraphs = soup.find_all("p")
        if not paragraphs:
            return []
        
        date = None
        for p in paragraphs[:3]:
            text = p.text.strip()
            date_match = re.search(r'\b[A-Z][a-z]+ \d{1,2}, \d{4}\b', text)
            if date_match:
                date = date_match.group()
                break

        data = []
        current_person = None

        for p in paragraphs:
            text = p.text.strip()
            if not text:
                continue

            speaker_match = re.match(r'^([A-Z\s]+):\s*(.+)$', text)
            if speaker_match:
                current_person = speaker_match.group(1).strip()
                quote = clean_text(speaker_match.group(2))
                if quote:
                    data.append([
                        event_name,
                        date or "Unknown Date",
                        current_person,
                        quote
                    ])
            
            elif current_person and text and not p.find("b"):
                data.append([
                    event_name,
                    date or "Unknown Date",
                    current_person,
                    clean_text(text)
                ])
        
        return data
    
    except Exception as e:
        print(f"Error scraping interview {interview_url}: {e}")
        return []


def main():
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)

            for event_url in event_urls:
                print(f"Processing event: {event_url}")
                event_date_links = get_event_date_links(event_url)

                for event_date_url in event_date_links:
                    interview_links = get_interview_links(event_date_url)

                    for interview_url in interview_links:
                        rows = scrape_interview(interview_url)
                        writer.writerows(rows)

        print(f"Data saved to {output_file}")
    
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
