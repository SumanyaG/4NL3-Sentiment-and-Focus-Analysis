import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import unicodedata

event_urls = ["https://www.asapsports.com/show_events.php?event_id=196462&category=11&year=2024&title=WNBA+DRAFT", 
              "https://www.asapsports.com/show_events.php?event_id=202524&category=11&year=2024&title=WNBA+FINALS%3A+MINNESOTA+VS.+NEW+YORK",
              "https://www.asapsports.com/show_events.php?event_id=198609&category=11&year=2024&title=NBA+DRAFT",
              "https://www.asapsports.com/show_events.php?event_id=198318&category=11&year=2024&title=NBA+FINALS%3A+CELTICS+VS.+MAVERICKS"] 

# URLs to ASAP Sports - WNBA Draft, WNBA Finals, NBA Draft, NBA Finals

output_file = "interviews.csv"
csv_headers = ["event", "date", "person", "quote"]

def fix_encoding(text):
    text = text.replace('‚Äô', "'")
    text = unicodedata.normalize('NFKD', text)

    return text

def extract_event_name(title):
    match = re.search('Basketball - (2024 - .+?) - [A-Z][a-z]+ \d+', title)
    if match:
        return match.group(1)
    return "Unknown Event"

def extract_date(title):
    match = re.search(r'- ([A-Z][a-z]+ \d+)', title)
    if match:
        return f"{match.group(1)}, 2024"
    return "Unknown Date"

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
    text = fix_encoding(text)
    return text.strip()

def is_question(text):
    question_indicators = [
        r'^\s*Q\.',
        r'\?\s*$',
        r'^(What|How|Why|When|Where|Who|Could|Can|Do|Does|Did|Is|Are|Was|Were)\s',
        r'^Tell us about',
        r'^Talk about'
    ]

    return any(re.search(pattern, text, re.IGNORECASE) for pattern in question_indicators)

def parse_speaker(text):
    speaker_pattern = r'^([A-Z][A-Za-z\s\'-]+(?:\s[A-Z][A-Za-z\'-]+)*):(.+)$'
    match = re.match(speaker_pattern, text)
    if match:
        speaker = match.group(1).strip()
        content = match.group(2).strip()
        return speaker, content
    return None, None

def scrape_interview(interview_url):
    try:
        response = requests.get(interview_url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title")
        if not title:
            return []

        title_text = title.text.strip()
        event_name = extract_event_name(title_text)
        date = extract_date(title_text)

        data = []
        current_person = None
        current_text = []
        in_question = False

        for p in soup.find_all("p"):
            text = p.text.strip()
            if not text:
                continue

            text = fix_encoding(text)

            if p.find("b") or is_question(text):
                if current_person and current_text:
                    combined_text = clean_text(" ".join(current_text))
                    data.append([event_name, date, current_person, combined_text])
                    current_text = []
                in_question = True
                continue

            speaker, content = parse_speaker(text)
            if speaker:
                if current_person and current_text and not in_question:
                    combined_text = clean_text(" ".join(current_text))
                    data.append([event_name, date, current_person, combined_text])
                
                current_person = speaker
                current_text = [content] if content else []
                in_question = False
            elif current_person and not in_question:
                current_text.append(text)

        if current_person and current_text and not in_question:
            combined_text = clean_text(" ".join(current_text))
            data.append([event_name, date, current_person, combined_text])

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
