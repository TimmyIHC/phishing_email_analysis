from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def send_email(subject, message_text, to):
    """Send an email from the user's account.

    Args:
      subject: Email subject as a string.
      message_text: Body of the email as a string, can be in HTML format.
      to: The recipient's email address as a string.
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created
    # automatically when the authorization flow completes for the first time.
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except FileNotFoundError:
        pass

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Create email message in HTML format
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['subject'] = subject
    part = MIMEText(message_text, 'html')
    message.attach(part)

    # Encode the message to base64
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {'raw': encoded_message}

    # Using the Gmail API to send the message.
    try:
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print("\033[34m - Message ID \033[0;0m %s" % send_message['id'])
        print("\033[34m - Email Sent Successfully \033[0;0m")
    except Exception as error:
        print('An error occurred: %s' % error)
