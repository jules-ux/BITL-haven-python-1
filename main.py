import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Laad omgevingsvariabelen uit .env-bestand
load_dotenv()

print(repr(os.getenv("FIREBASE_ADMIN_PRIVATE_KEY")))

# Verzamel gegevens uit omgevingsvariabelen
service_account = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_ADMIN_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_ADMIN_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_ADMIN_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_ADMIN_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_ADMIN_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_ADMIN_CLIENT_X509_CERT_URL"),
}

# Initialiseer Firebase-app met de serviceaccountgegevens
cred = credentials.Certificate(service_account)
firebase_admin.initialize_app(cred)

def add_item_to_firestore(collection_name, document_id, data):
    """
    Voeg een item toe aan een specifieke collectie in Firestore.

    :param collection_name: Naam van de Firestore-collectie.
    :param document_id: ID van het document (of None voor automatisch gegenereerde ID).
    :param data: Dictionary met gegevens om toe te voegen.
    :return: Document ID van het toegevoegde item.
    """
    db = firestore.client()
    collection_ref = db.collection(collection_name)

    if document_id:
        collection_ref.document(document_id).set(data)
        return document_id
    else:
        doc_ref = collection_ref.add(data)
        return doc_ref[1].id

# Voorbeeldgebruik
if __name__ == "__main__":
    collection = "users"
    document_id = None  # Laat leeg voor automatisch gegenereerde ID
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
    }

    doc_id = add_item_to_firestore(collection, document_id, user_data)
    print(f"Document toegevoegd met ID: {doc_id}")
