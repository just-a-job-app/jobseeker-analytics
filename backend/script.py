import os
import json
import base64
import email
import re
from datetime import datetime
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import pandas as pd
import tempfile
import webbrowser
import html2text

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def clean_whitespace(text: str) -> str:
    """Remove excessive whitespace while preserving paragraph breaks."""
    # Replace multiple newlines with a single one
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Remove leading/trailing whitespace from each line
    text = '\n'.join(line.strip() for line in text.split('\n'))
    return text.strip()

def clean_email_content(text: str) -> str:
    """Clean up email content by extracting only text content."""
    # Use BeautifulSoup to extract only text content
    soup = BeautifulSoup(text, 'html.parser')
    
    # Remove all style and script tags
    for tag in soup.find_all(['style', 'script']):
        tag.decompose()
    
    # Get only the text content
    text = soup.get_text(separator=' ', strip=True)
    
    # Remove any remaining CSS-like content
    text = re.sub(r'@media[^{]*{[^}]*}', '', text)  # Remove media queries
    text = re.sub(r'{[^}]*}', '', text)  # Remove CSS blocks
    text = re.sub(r'!important', '', text)  # Remove !important declarations
    text = re.sub(r'\*\[[^\]]*\]', '', text)  # Remove attribute selectors
    text = re.sub(r'\.[a-zA-Z0-9_-]+', '', text)  # Remove class selectors
    text = re.sub(r'/\*[^*]*\*/', '', text)  # Remove CSS comments
    text = re.sub(r'}\s*}', '', text)  # Remove closing braces
    text = re.sub(r',\s*,', ',', text)  # Remove duplicate commas
    
    # Remove tracking URLs and parameters
    text = re.sub(r'http://[^\s)]+', '', text)  # Remove http URLs
    text = re.sub(r'https://[^\s)]+', '', text)  # Remove https URLs
    text = re.sub(r'\([^)]*\)', '', text)  # Remove parenthetical content
    text = re.sub(r'\[[^\]]*\]', '', text)  # Remove bracketed content
    
    # Clean up whitespace and punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    text = re.sub(r',\s*$', '', text)  # Remove trailing commas
    text = re.sub(r'^\s*,\s*', '', text)  # Remove leading commas
    text = re.sub(r'\s*,\s*', ', ', text)  # Normalize comma spacing
    text = text.strip()
    
    return text

class GmailDataCollector:
    def __init__(self, credentials_path: str = 'credentials.json'):
        """
        Initialize the Gmail data collector.
        
        Args:
            credentials_path: Path to the Google OAuth credentials file
        """
        self.credentials_path = credentials_path
        self.service = self._get_gmail_service()
        # Get user's email address
        profile = self.service.users().getProfile(userId='me').execute()
        self.user_email = profile['emailAddress']
        
    def _get_gmail_service(self):
        """Set up Gmail API service with authentication."""
        creds = None
        
        # Check if token.json exists (saved credentials)
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=50089)
                
            # Save credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                
        return build('gmail', 'v1', credentials=creds)
    
    def search_emails(self, query: str, after_date: str = "2024/01/01") -> List[str]:
        """
        Search for all email message IDs matching the query and after a given date.
        Handles pagination to retrieve all results.
        Returns a list of message IDs.
        """
        all_message_ids = []
        page_token = None
        # Add date filter to query
        full_query = f"{query} after:{after_date.replace('-', '/')}"
        while True:
            response = self.service.users().messages().list(
                userId='me',
                q=full_query,
                maxResults=500,  # Gmail API max is 500
                pageToken=page_token
            ).execute()
            messages = response.get('messages', [])
            all_message_ids.extend([msg['id'] for msg in messages])
            page_token = response.get('nextPageToken')
            if not page_token:
                break
        return all_message_ids
    
    def view_full_email_html(self, html_content: str):
        """Open the full email HTML in a temporary browser window."""
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            f.write("""
            <html>
            <head>
                <style>
                    body { 
                        max-width: 800px; 
                        margin: 40px auto; 
                        padding: 20px;
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                    }
                </style>
            </head>
            <body>
            """)
            f.write(html_content)
            f.write("</body></html>")
            temp_path = f.name
        
        webbrowser.open('file://' + temp_path)
        return temp_path

    def get_email_content(self, message_id: str) -> Dict:
        """
        Get the full content of an email.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary containing email content and metadata
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            # Get email headers
            headers = message['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'] == 'Subject')
            sender = next(h['value'] for h in headers if h['name'] == 'From')
            date = next(h['value'] for h in headers if h['name'] == 'Date')
            
            # Skip if the email is from the user (check both email and name)
            if (self.user_email in sender or 
                "Lianna Novitz" in sender or 
                "lianna.novitz" in sender.lower()):
                return None
            
            # Get email body
            body = ''
            html_content = ''
            
            def decode_base64(data):
                try:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
                except Exception as e:
                    print(f"Error decoding base64: {e}")
                    return ''

            def extract_content(part):
                if 'body' in part and 'data' in part['body']:
                    return decode_base64(part['body']['data'])
                return ''

            def process_parts(parts):
                nonlocal body, html_content
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        body = extract_content(part)
                    elif part['mimeType'] == 'text/html':
                        html_content = extract_content(part)
                    elif 'parts' in part:
                        process_parts(part['parts'])
            
            if 'parts' in message['payload']:
                process_parts(message['payload']['parts'])
            else:
                # Handle single part message
                if message['payload']['mimeType'] == 'text/plain':
                    body = extract_content(message['payload'])
                elif message['payload']['mimeType'] == 'text/html':
                    html_content = extract_content(message['payload'])
                    body = BeautifulSoup(html_content, 'html.parser').get_text()
            
            # If we still don't have a body, try to get it from the raw message
            if not body and not html_content:
                raw_message = self.service.users().messages().get(
                    userId='me',
                    id=message_id,
                    format='raw'
                ).execute()
                if 'raw' in raw_message:
                    raw_data = base64.urlsafe_b64decode(raw_message['raw'])
                    email_message = email.message_from_bytes(raw_data)
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode()
                            elif part.get_content_type() == 'text/html':
                                html_content = part.get_payload(decode=True).decode()
                    else:
                        body = email_message.get_payload(decode=True).decode()
            
            # If we have HTML but no plain text, convert HTML to text
            if not body and html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                body = soup.get_text()
            
            # Clean up the content
            body = clean_email_content(body)
            if html_content:
                html_content = clean_email_content(html_content)
            
            # Store HTML content separately for viewing during labeling
            self._current_html_content = html_content if html_content else f"<html><body><pre>{body}</pre></body></html>"
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body
            }
            
        except Exception as e:
            print(f"Error getting email content: {e}")
            return None
    
    def load_labeled_message_ids(self, output_file: str = 'training_data.json') -> set:
        """
        Load already labeled message IDs from the output file.
        """
        if not os.path.exists(output_file):
            return set()
        with open(output_file, 'r') as f:
            try:
                data = json.load(f)
                return set(email['id'] for email in data if 'id' in email)
            except Exception:
                return set()
    

    def collect_training_data(self, output_file: str = 'training_data.json'):
        """
        Collect and label training data from Gmail, skipping already labeled messages.
        """
        # Check if user wants to start fresh
        if os.path.exists(output_file):
            choice = input("Existing training data found. Delete and start fresh? (y/n): ")
            if choice.lower() == 'y':
                os.remove(output_file)
                print("Deleted existing training data.")
            else:
                print("Continuing with existing data.")

        # Search query for job application related emails
        with open("start_date_query.txt", "r") as f:
            query = f.read()
        
        # Get all message IDs since Jan 1, 2024
        message_ids = self.search_emails(query, after_date="2024/01/01")
        labeled_ids = self.load_labeled_message_ids(output_file)
        training_data = []
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                training_data = json.load(f)

        print(f"Found {len(message_ids)} potential job application emails since 2024-01-01")
        
        statuses = [
            "False positive, not related to job search",
            "Application confirmation",
            "Rejection",
            "Availability request", # Action required from candidate
            "Information request",  # Action required from candidate
            "Assessment sent", # Action required from candidate
            "Interview invitation", # Action required from candidate
            "Informational outreach", # Action required from candidate
            "Did not apply - inbound request", # Action required from candidate
            "Action required from company",
            "Hiring freeze notification",
            "Withdrew application",
            "Offer made",  # Action required from candidate
            "Offer negotiated",
            "Offer accepted",
            "Offer rejected",
            "Offer rescinded",
        ]

        temp_html_file = None

        try:
            for i, msg_id in enumerate(message_ids, 1):
                if msg_id in labeled_ids:
                    print(f"Skipping already labeled message {msg_id}")
                    continue
                
                email_data = self.get_email_content(msg_id)
                if not email_data:
                    continue

                print("\n" + "="*80)
                print(f"Email {i}/{len(message_ids)}")
                print("="*80)
                print(f"Subject: {email_data['subject']}")
                print(f"From: {email_data['sender']}")
                print(f"Date: {email_data['date']}")
                print("\nBody preview (first 500 characters):")
                print("-"*80)
                print(email_data['body'][:500])
                print("\n... (press 'v' to view full email in browser) ...")
                
                # Get user input for labeling
                while True:
                    print("\nPossible statuses:")
                    for j, status in enumerate(statuses, 1):
                        print(f"{j}. {status}")
                    print("v. View full email in browser")
                    
                    choice = input("\nEnter choice (number or 'v' for view): ").strip().lower()
                    
                    if choice == 'v':
                        if temp_html_file:  # Clean up previous temp file if it exists
                            try:
                                os.unlink(temp_html_file)
                            except:
                                pass
                        temp_html_file = self.view_full_email_html(self._current_html_content)
                        continue
                    
                    try:
                        choice = int(choice)
                        if 1 <= choice <= len(statuses):
                            email_data['application_status'] = statuses[choice - 1]
                            training_data.append(email_data)
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Please enter a valid number or 'v'.")
                
                # Save progress after each email
                with open(output_file, 'w') as f:
                    json.dump(training_data, f, indent=2)
                
                print(f"\nProgress saved. {len(training_data)} emails labeled so far.")
                
                # Clean up temp file if it exists
                if temp_html_file and os.path.exists(temp_html_file):
                    try:
                        os.unlink(temp_html_file)
                        temp_html_file = None
                    except:
                        pass

        finally:
            # Ensure temp file cleanup on exit
            if temp_html_file and os.path.exists(temp_html_file):
                try:
                    os.unlink(temp_html_file)
                except:
                    pass
            
        print(f"\nData collection complete. {len(training_data)} emails labeled.")
        print(f"Data saved to {output_file}")

         # Save all data to the main file
        with open(output_file, 'w') as f:
            json.dump(training_data, f, indent=2)

        # Split data by category
        false_positives = [email for email in training_data if email.get('application_status') == "False positive, not related to job search"]
        applications = [email for email in training_data if email.get('application_status') != "False positive, not related to job search"]

        # Save false positives
        with open("training_data_false_positive.json", "w") as f:
            json.dump(false_positives, f, indent=2)
        print(f"Saved {len(false_positives)} false positives to training_data_false_positive.json")

        # Save all other applications
        with open("training_data_applications.json", "w") as f:
            json.dump(applications, f, indent=2)
        print(f"Saved {len(applications)} application-related emails to training_data_applications.json")

        
        # Convert to CSV for easier analysis
        df = pd.DataFrame(training_data)
        csv_file = output_file.replace('.json', '.csv')
        df.to_csv(csv_file, index=False)
        print(f"Data also saved to {csv_file}")

def main():
    # Initialize the collector
    collector = GmailDataCollector()
    
    # Start collecting data
    collector.collect_training_data()

if __name__ == "__main__":
    main()