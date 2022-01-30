import json
import logging

from google.cloud import firestore, storage


def upload_document_to_firestore_database(
    collection_path: str, document_id: str, data: dict, merge: bool = True
) -> None:
    try:
        # Write document
        firestore.Client().collection(collection_path).document(document_id).set(
            data, merge=merge
        )
    except Exception as e:
        # Swallow all exceptions and log
        logging.warning(f"An exception occured: { e }")


def get_file_from_storage(filename: str) -> json:
    storage_client = storage.Client()
    bucket = storage_client.bucket("market-prediction-5209e.appspot.com")
    blob = bucket.blob(filename)
    data = blob.download_as_string().decode("utf-8")

    return json.loads(data)
