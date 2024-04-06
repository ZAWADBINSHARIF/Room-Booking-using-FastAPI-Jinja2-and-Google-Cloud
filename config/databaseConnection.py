# external import
from google.cloud import firestore
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file(
    "config/room-booking-2f8ca-firebase-adminsdk-ezo1w-8a9c49b5d5.json"
)

db = firestore.Client(credentials=credentials)
