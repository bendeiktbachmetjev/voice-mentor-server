import firebase_admin
from firebase_admin import credentials, messaging
import os
from pathlib import Path

# Путь к файлу сервисного аккаунта
service_account_path = os.path.join(Path(__file__).parent.parent, 'firebase-service-account.json')

# Инициализация Firebase
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    
    try:
        response = messaging.send(message)
        return {"success": True, "message_id": response}
    except Exception as e:
        return {"success": False, "error": str(e)} 