# Upload an image to the firebase storage
import firebase_admin
from firebase_admin import credentials, storage
import datetime

cred = credentials.Certificate('auth/iedcampus-firebase-adminsdk-fbsvc-48b145a483.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'iedcampus.firebasestorage.app'
})

bucket = storage.bucket()

blobs = bucket.list_blobs()

now = datetime.datetime.now(datetime.timezone.utc)
one_day_ago = now - datetime.timedelta(hours=14) # 14 horas es buen numero para borrar lo de ayer, pero no lo de hoy

counter = 0

for blob in blobs: 
    if counter == 0:
        if blob.time_created > one_day_ago:
            blob.delete()
            counter += 1

print(str(counter) + " imagenes borradas en firebase")
