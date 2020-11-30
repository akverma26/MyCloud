import pickle
import os
import time

from MyCloud.settings import BASE_DIR

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def create_google_api_service(
    SCOPES: list,
    serviceName: str,
    version: str,
    token_file: str,
    credentials_file: str
):
    """
    Create any Google API Service.
    This is the basic code in python to create a Google API Service.

    :param SCOPES: List of scopes for which the service is to be created
    :param serviceName: Name of the service to be created
    :param version: Version of the service to be created
    :token_file: Path to token.pickle file
    :credentials_file: Path to credentials.json file
    :return: Google API Service instance that is created

    Ex: Creating Google Drive service instance
    create_google_api_service(
        ['https://www.googleapis.com/auth/drive.metadata.readonly'],
        'drive',
        'v3',
        'token.pickle',
        'credentials.json'
    )
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build(serviceName, version, credentials=creds)
    return service


def get_drive_files_list(socket):
    socket.send(text_data="Creating service...")
    service = create_google_api_service(
        ['https://www.googleapis.com/auth/drive.metadata.readonly'],
        'drive',
        'v3',
        os.path.join(BASE_DIR, 'token.pickle'),
        os.path.join(BASE_DIR, 'credentials.json')
    )
    socket.send(text_data="Service created...")
    socket.send(text_data="Fetching Data...")

    results = service.files().list(
        pageSize=30, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    socket.send(text_data="Data Fetched.")

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            socket.send(text_data=u'{0} ({1})'.format(
                item['name'], item['id']))
            time.sleep(5)
    socket.send("Done")
