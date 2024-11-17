import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate("D:/Social-Media-App/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_notification(token, title, body):
    message = messaging.Message(
        data={"title": title, "body": body},
        token=token,
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)

    