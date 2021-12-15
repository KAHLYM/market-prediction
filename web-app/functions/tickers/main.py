import json

import pandas as pd
from google.cloud import storage


class Index:
    def __init__(self, name: str, source: str, columns: list):
        self.name = name
        self.source = source
        self.columns = columns

        self.data = {}

        self.extract_from_table()
        self.upload_to_storage()

    def format_security_name(self, security_name: str) -> str:
        # Remove text that specifies share type
        security_name = security_name.split(" -", 1)[0]

        legal_structure_identifiers = [
            ("Corporation", "Corp"),
            ("Incorporated", "Inc"),
            ("Public Limited Company", "Plc"),
            ("Limited", "Ltd"),
        ]

        # Remove text that specifies legal structure
        for legal_structure_identifier in legal_structure_identifiers:
            # fmt: off
            security_name = security_name.replace(legal_structure_identifier[0], '')                # Public Limited Company
            security_name = security_name.replace(legal_structure_identifier[1].title() + '.', '')  # Plc.
            security_name = security_name.replace(legal_structure_identifier[1].lower() + '.', '')  # plc.
            security_name = security_name.replace(legal_structure_identifier[1].upper() + '.', '')  # PLC.
            security_name = security_name.replace(legal_structure_identifier[1].title(), '')        # Plc
            security_name = security_name.replace(legal_structure_identifier[1].lower(), '')        # plc
            security_name = security_name.replace(legal_structure_identifier[1].upper(), '')        # PLC
            # fmt: on

        # Remove trailing punctuation/whitespace
        security_name = security_name.replace(",", "")
        security_name = security_name.strip()

        return security_name

    def extract_from_table(self) -> None:
        # Retrieve source data and extract table
        table = pd.read_html(self.source)[0]
        df = pd.DataFrame(table, columns=self.columns)

        # Generate Symbol-SecurityName dictionary
        for row in df.itertuples():
            self.data[row[1]] = self.format_security_name(row[2])

    def upload_to_storage(self) -> None:
        storage_client = storage.Client()
        bucket = storage_client.bucket("market-prediction-5209e.appspot.com")
        blob = bucket.blob(self.name)
        blob.upload_from_string(json.dumps(self.data))


def tickers(event, context):
    IndexSP500: Index = Index("sp500", "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", ["Symbol", "Security"])
