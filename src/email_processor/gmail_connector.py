"""
Gmail Connector Module

This module handles Gmail API authentication and email operations for alfredAI.
It provides functionality to connect to Gmail, fetch emails, and manage email processing.
"""

import os
import pickle
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from loguru import logger
import base64
import os.path

class GmailConnector:
    """
    Handles Gmail API connections and email operations.
    """
    
    # If modifying these scopes, delete the token.pickle file.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_path: str = 'config/gmail_credentials.json'):
        """
        Initialize the Gmail connector.
        
        Args:
            credentials_path (str): Path to the Gmail API credentials file
        """
        self.credentials_path = credentials_path
        self.service = None
        self.creds = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth 2.0.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Check if we have valid credentials
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            
            # If no valid credentials available, let user log in
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token, protocol=4)
            
            # Build the Gmail API service
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
    
    def fetch_unread_emails(self, max_results: int = 10) -> List[Dict]:
        """
        Fetch unread emails from Gmail.
        
        Args:
            max_results (int): Maximum number of emails to fetch
            
        Returns:
            List[Dict]: List of email messages with their details
        """
        try:
            if not self.service:
                raise ValueError("Gmail service not initialized. Call authenticate() first.")
            
            # Search for unread emails
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []
            
            for message in messages:
                email_data = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Extract relevant email details
                email_details = self._parse_email_data(email_data)
                email_list.append(email_details)
            
            return email_list
            
        except HttpError as error:
            logger.error(f"Error fetching emails: {str(error)}")
            return []
    
    def _parse_email_data(self, email_data: Dict) -> Dict:
        """
        Parse raw email data into a structured format.
        
        Args:
            email_data (Dict): Raw email data from Gmail API
            
        Returns:
            Dict: Structured email data
        """
        headers = email_data['payload']['headers']
        
        # Extract email metadata
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # Extract email body
        body = self._get_email_body(email_data['payload'])
        
        # Add attachment handling
        attachments = self._get_attachments(email_data['payload'])
        
        return {
            'id': email_data['id'],
            'threadId': email_data['threadId'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body,
            'attachments': attachments
        }
    
    def _get_email_body(self, payload: Dict) -> str:
        """
        Extract email body from payload.
        
        Args:
            payload (Dict): Email payload data
            
        Returns:
            str: Email body text
        """
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return self._decode_body(part['body'])
        elif payload['mimeType'] == 'text/plain':
            return self._decode_body(payload['body'])
        return ""
    
    def _decode_body(self, body: Dict) -> str:
        """
        Decode email body content.
        
        Args:
            body (Dict): Email body data
            
        Returns:
            str: Decoded email body text
        """
        if 'data' in body:
            return base64.urlsafe_b64decode(body['data']).decode('utf-8')
        return ""

    def _get_attachments(self, payload: Dict) -> List[Dict]:
        """
        Extract attachments from email payload.
        
        Args:
            payload (Dict): Email payload data
            
        Returns:
            List[Dict]: List of attachment details with filename and data
        """
        attachments = []
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = self.service.users().messages().attachments().get(
                            userId='me',
                            messageId=payload['id'],
                            id=att_id
                        ).execute()
                        data = att['data']
                    
                    attachments.append({
                        'filename': part['filename'],
                        'data': base64.urlsafe_b64decode(data),
                        'mimeType': part['mimeType']
                    })
                
        return attachments

    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark an email as read.
        
        Args:
            message_id (str): Gmail message ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking message as read: {str(e)}")
            return False 