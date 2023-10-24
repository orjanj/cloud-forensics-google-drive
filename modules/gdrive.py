# Reimplementation of code from Google with some changes: https://developers.google.com/drive/api/quickstart/python#recommendations-link

from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.appdata']


class GoogleDrive:
    def __init__(
            self, credentials_file, token_file):
        """ Initialize connection to Google Drive.
        :params credentials_file: Credential file (path)
        """
        self.credentials_path = credentials_file
        self.token_path = token_file
        self.refresh_user_token()


    def refresh_user_token(
            self):
        """ Refresh user tokens and store user's access."""
        self.creds = None
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if (not self.creds or
            not self.creds.valid):
            if (self.creds and 
                self.creds.expired and
                self.creds.refresh_token):
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

    def connect(
            self, drive_display_name):
        try:
            self.service = build('drive', 'v3', credentials=self.creds)
            results = self.service.about().get(fields="*").execute()

            # Verify the display name is correct
            if drive_display_name == results['user']['displayName']:
                pass
                # print("Connected to Google Drive.")
            else:
                print(f"Error: Connection error.")
                sys.exit(1)

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')


    def list_files(
            self, metadata = None, print_output = False):
        """ List files from Google Drive. """
        if metadata is True:
            results = self.service.files().list(
                pageSize=10, fields="*").execute()
        else:
            results = self.service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            if print_output:
                print('No files found.')
            return
        for item in items:
            if (print_output and
                metadata):
                print(json.dumps(item, indent=2))
            elif metadata:
                return json.dumps(item, indent=2)
            else:
                print(f"{item['name']} ({item['id']})")

    def get_start_page_token(
            self):
        """ Get start page token. """
        try:
            start_page_token = self.service.changes().getStartPageToken().execute()
        except HttpError as error:
            start_page_token = None
        return start_page_token.get('startPageToken')

    def list_changes(
            self, start_page_token = None):
        """ Get disk changes. """
        try:
            page_token = start_page_token

            changes = []
            while page_token is not None:
                response = self.service.changes().list(
                    pageToken=page_token,
                    fields="*",
                    spaces='drive').execute()

                changes.extend(response.get('changes'))

                if 'newStartPageToken' in response:
                    # Last page, save this token for the next polling interval
                    start_page_token = response.get('newStartPageToken')
                page_token = response.get('nextPageToken')

            json_blob = json.dumps(changes, indent=2)

        except HttpError as error:
            print(f"Error occured: {error}")
            start_page_token = None

        return json_blob