import os 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#Read only cal acess

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_cal_service():
    """
    Auth the user and return a google calendar api srvice --> open browser on first run 
    creates token after good auth
    """

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    #If no valid creds
    if not creds or not creds.valid:
        if creds and creds.expired and creds.rapt_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    service = build("calendar", "v3", credentials=creds)

    return service 