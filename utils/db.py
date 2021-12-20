import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
#SPREADSHEET_ID = "1rkMVLvh3JrBq_tbi4Ho0qjCDAP3vYdNuWOEjYpkJLNU"
SPREADSHEET_ID = "1-seXiY5a1NuMNwURA409Q6u2g8ZQo843xMJku7mV6Q0"
SHEET_NAME = "일지기록"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"


@st.experimental_singleton()
def connect():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    service = build("sheets", "v4", credentials=credentials)
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def collect(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:C",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def insert(gsheet_connector, row) -> None:
    values = (
        gsheet_connector.values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:C",
            body=dict(values=row),
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )
