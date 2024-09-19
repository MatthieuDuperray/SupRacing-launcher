from __future__ import print_function

import os

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials


def add(spreadsheet_id, range, values, value_input_option='USER_ENTERED'):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """

    if os.path.exists('./sheet_log/token.json'):
        creds = Credentials.from_authorized_user_file('./sheet_log/token.json')
        # pylint: disable=maybe-no-member

    try:

        service = build('sheets', 'v4', credentials=creds)
        
        body = {
            'values': values
        }

        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range, body=body, valueInputOption=value_input_option
        ).execute()

        return result
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: spreadsheet_id,  range_name, value_input_option and  _values
    add("1f-Myu8fBzV055cakvrHinSlJi9xiJ_ICsK2a6rLDbGA", 'Feuille 1!A:C',[["a", 'b', 45]])