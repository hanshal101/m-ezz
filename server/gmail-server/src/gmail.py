from typing import Any, List, Dict, Optional
from mcp.server.fastmcp import FastMCP 
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailAPI:
    """Gmail API Class (from your provided code) - No changes here"""
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.modify' #Needed for deleting and marking as read/unread
    ]

    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.creds = None
        self.token_file = token_file
        self.credentials_file = credentials_file

        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=50505) #changes made here for a fixed port
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())
        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
        except HttpError as error:
            print(f'An error occurred during service initialization: {error}')
            self.service = None

    def send_message(self, to, subject, message_text, attachments=None, cc=None, bcc=None):
        # ... (rest of your send_message method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot send message.")
            return None

        message = MIMEMultipart()
        if isinstance(to, str):
            message['to'] = to
        elif isinstance(to, list):
            message['to'] = ', '.join(to)
        else:
            raise TypeError("'to' must be a string or a list of strings")

        if cc:
            if isinstance(cc, str):
                message['cc'] = cc
            elif isinstance(cc, list):
                message['cc'] = ', '.join(cc)
            else:
                raise TypeError("'cc' must be a string or a list of strings")

        if bcc:
            if isinstance(bcc, str):
                message['bcc'] = bcc
            elif isinstance(bcc, list):
                message['bcc'] = ', '.join(bcc)
            else:
                raise TypeError("'bcc' must be a string or a list of strings")

        message['subject'] = subject
        msg = MIMEText(message_text, 'plain') # 'plain' for plain text, 'html' for HTML content
        message.attach(msg)


        if attachments:
            for attachment_path in attachments:
                if not os.path.exists(attachment_path):
                    raise FileNotFoundError(f"Attachment file not found: {attachment_path}")

                content_type, encoding = mimetypes.guess_type(attachment_path)
                if content_type is None or encoding is not None:
                    content_type = 'application/octet-stream'

                main_type, sub_type = content_type.split('/', 1)
                with open(attachment_path, 'rb') as fp:
                    if main_type == 'text':
                        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
                    elif main_type == 'image':
                        msg = MIMEImage(fp.read(), _subtype=sub_type)
                    elif main_type == 'audio':
                        msg = MIMEAudio(fp.read(), _subtype=sub_type)
                    else:
                        msg = MIMEBase(main_type, sub_type)
                        msg.set_payload(fp.read())

                filename = os.path.basename(attachment_path)
                msg.add_header('Content-Disposition', 'attachment', filename=filename)
                message.attach(msg)


        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            send_message = (self.service.users().messages().send
                            (userId="me", body={'raw': raw_message}))
            response = send_message.execute()
            print(f"Message sent successfully. Message Id: {response['id']}")
            return response
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def search_messages(self, query):
        # ... (rest of your search_messages method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot search messages.")
            return None

        try:
            response = self.service.users().messages().list(userId='me', q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def get_message(self, message_id, format='full'):
        # ... (rest of your get_message method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot get message.")
            return None
        try:
            message = self.service.users().messages().get(userId='me', id=message_id, format=format).execute()
            return message
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def get_message_details(self, message_id):
        # ... (rest of your get_message_details method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot get message details.")
            return None

        message = self.get_message(message_id)
        if not message:
            return None

        payload = message['payload']
        headers = payload['headers']

        details = {
            'Date': [h['value'] for h in headers if h['name'] == 'Date'][0],
            'Sender': [h['value'] for h in headers if h['name'] == 'From'][0],
            'Subject': [h['value'] for h in headers if h['name'] == 'Subject'][0],
            'Snippet': message['snippet'],
            'Body': ""  # Initialize Body
        }
        # Function to decode email body
        def get_body(payload):
            data = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    data += get_body(part)
            elif 'body' in payload and 'data' in payload['body']:
                try:
                    data = base64.urlsafe_b64decode(payload['body']['data']).decode()
                except Exception as e:
                    print(f"Error decoding body: {e}") # Keep as print for the example class.
            return data

        details['Body'] = get_body(payload)
        return details

    def mark_as_read(self, message_id):
        # ... (rest of your mark_as_read method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot mark message as read.")
            return None

        try:
            response = self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return response
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def mark_as_unread(self, message_id):
        # ... (rest of your mark_as_unread method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot mark message as unread.")
            return None

        try:
            response = self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            return response
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def delete_message(self, message_id):
        # ... (rest of your delete_message method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot delete message.")
            return None

        try:
            response = self.service.users().messages().trash(userId='me', id=message_id).execute()
            return response
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def create_draft(self, to, subject, message_text, attachments=None):
        # ... (rest of your create_draft method - no changes) ...
        if not self.service:
            print("Gmail service not initialized. Cannot create draft.")
            return None

        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        msg = MIMEText(message_text)
        message.attach(msg)

        if attachments:
            for attachment_path in attachments:
                if not os.path.exists(attachment_path):
                    raise FileNotFoundError(f"Attachment file not found: {attachment_path}")

                content_type, encoding = mimetypes.guess_type(attachment_path)
                if content_type is None or encoding is not None:
                    content_type = 'application/octet-stream'

                main_type, sub_type = content_type.split('/', 1)
                with open(attachment_path, 'rb') as fp:
                    if main_type == 'text':
                        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
                    elif main_type == 'image':
                        msg = MIMEImage(fp.read(), _subtype=sub_type)
                    elif main_type == 'audio':
                        msg = MIMEAudio(fp.read(), _subtype=sub_type)
                    else:
                        msg = MIMEBase(main_type, sub_type)
                        msg.set_payload(fp.read())

                filename = os.path.basename(attachment_path)
                msg.add_header('Content-Disposition', 'attachment', filename=filename)
                message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            draft = self.service.users().drafts().create(userId="me", body={'message': {'raw': raw_message}}).execute()
            print(f"Draft created successfully. Draft Id: {draft['id']}")
            return draft
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None


# Initialize FastMCP server
mcp = FastMCP("gmail")

# Instantiate Gmail API
gmail_api = GmailAPI() # Ensure credentials.json and token.json are in the same directory or provide paths

@mcp.tool()
async def send_email_tool(to: str, subject: str, message_text: str, attachments: Optional[List[str]] = None, cc: Optional[str] = None, bcc: Optional[str] = None) -> str:
    """Send an email using Gmail.

    Args:
        to: Recipient email address.
        subject: Subject of the email.
        message_text: Body of the email (plain text).
        attachments: Optional list of file paths to attach.
        cc: Optional CC recipient email address.
        bcc: Optional BCC recipient email address.
    """
    try:
        response = gmail_api.send_message(to=to, subject=subject, message_text=message_text, attachments=attachments, cc=cc, bcc=bcc)
        if response and 'id' in response:
            return f"Email sent successfully. Message ID: {response['id']}"
        else:
            return "Failed to send email. Check server logs for details."
    except Exception as e:
        return f"Error sending email: {e}"

@mcp.tool()
async def search_emails_tool(query: str) -> str:
    """Search emails in Gmail.

    Args:
        query: Gmail search query (e.g., 'from:sender@example.com subject:keyword').
    """
    try:
        messages = gmail_api.search_messages(query)
        if messages:
            message_ids = [msg['id'] for msg in messages]
            return f"Found {len(message_ids)} emails matching query. Message IDs: {', '.join(message_ids)}"
        else:
            return "No emails found matching the query."
    except Exception as e:
        return f"Error searching emails: {e}"

@mcp.tool()
async def get_email_details_tool(message_id: str) -> str:
    """Get details of a specific email from Gmail.

    Args:
        message_id: The ID of the email to retrieve details for.
    """
    try:
        details = gmail_api.get_message_details(message_id)
        if details:
            formatted_details = "\n".join([f"{key}: {value}" for key, value in details.items()])
            return f"Email Details:\n{formatted_details}"
        else:
            return f"Could not retrieve details for email ID: {message_id}"
    except Exception as e:
        return f"Error getting email details: {e}"

@mcp.tool()
async def mark_email_read_tool(message_id: str) -> str:
    """Mark an email as read in Gmail.

    Args:
        message_id: The ID of the email to mark as read.
    """
    try:
        response = gmail_api.mark_as_read(message_id)
        if response:
            return f"Email marked as read. Message ID: {message_id}"
        else:
            return f"Failed to mark email as read. Message ID: {message_id}"
    except Exception as e:
        return f"Error marking email as read: {e}"

@mcp.tool()
async def mark_email_unread_tool(message_id: str) -> str:
    """Mark an email as unread in Gmail.

    Args:
        message_id: The ID of the email to mark as unread.
    """
    try:
        response = gmail_api.mark_as_unread(message_id)
        if response:
            return f"Email marked as unread. Message ID: {message_id}"
        else:
            return f"Failed to mark email as unread. Message ID: {message_id}"
    except Exception as e:
        return f"Error marking email as unread: {e}"

@mcp.tool()
async def delete_email_tool(message_id: str) -> str:
    """Delete an email in Gmail (moves to trash).

    Args:
        message_id: The ID of the email to delete.
    """
    try:
        response = gmail_api.delete_message(message_id)
        if response:
            return f"Email moved to trash. Message ID: {message_id}"
        else:
            return f"Failed to delete email. Message ID: {message_id}"
    except Exception as e:
        return f"Error deleting email: {e}"

@mcp.tool()
async def create_email_draft_tool(to: str, subject: str, message_text: str, attachments: Optional[List[str]] = None) -> str:
    """Create a draft email in Gmail (does not send).

    Args:
        to: Recipient email address for the draft.
        subject: Subject of the draft email.
        message_text: Body of the draft email (plain text).
        attachments: Optional list of file paths to attach to the draft.
    """
    try:
        draft = gmail_api.create_draft(to=to, subject=subject, message_text=message_text, attachments=attachments)
        if draft and 'id' in draft:
            return f"Draft email created successfully. Draft ID: {draft['id']}"
        else:
            return "Failed to create email draft. Check server logs for details."
    except Exception as e:
        return f"Error creating email draft: {e}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')