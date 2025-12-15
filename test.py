import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

KEY_PATH = "./firestore/firebase-adminsdk.json"

def main():
    if not firebase_admin._apps:
        cred = credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    # Firestore write 테스트
    doc_ref = db.collection("test").document("hello")
    doc_ref.set({
        "msg": "Firestore 연결 성공!",
        "created_at": datetime.utcnow().isoformat()
    })

    # read 테스트
    snap = doc_ref.get()
    print("READ RESULT:", snap.to_dict())

if __name__ == "__main__":
    main()