import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email import policy
from email.parser import BytesParser


# Authenticate with Gmail API


def gmail_authenticate():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.modify']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service


# Get unread emails and extract attachments (EML files)
def get_unread_emails(service):
    response = service.users().messages().list(userId='me', q='is:unread', maxResults=1).execute()
    messages = response.get('messages', [])

    emails_info = []

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

        eml_content = None
        for part in msg['payload']['parts']:
            if part['filename'].endswith('.eml'):
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'],
                                                                          id=attachment_id).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                eml_content = file_data
                break

        if eml_content:
            email_info = parse_eml(eml_content)
            email_info.update({"message_id": message['id']})
            emails_info.append(email_info)

    return emails_info


# Parse EML content including detailed headers
def parse_eml(eml_content):
    parser = BytesParser(policy=policy.default)
    email_obj = parser.parsebytes(eml_content)

    headers_interest = ['DKIM-Signature', 'Received-SPF', 'Authentication-Results', 'Return-Path', 'Received']
    interesting_headers = {key: email_obj[key] for key in headers_interest if key in email_obj}

    email_info = {
        "from": email_obj['from'],
        "to": email_obj['to'],
        "subject": email_obj['subject'],
        "date": email_obj['date'],
        "body": email_obj.get_body(preferencelist=('plain')).get_content(),
        "interesting_headers": interesting_headers
    }

    return email_info


def mark_email_as_read(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
