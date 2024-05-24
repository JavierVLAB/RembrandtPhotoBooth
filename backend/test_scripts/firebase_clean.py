# Upload an image to the firebase storage
import firebase_admin
from firebase_admin import credentials, storage
import datetime

cred = credentials.Certificate('../auth/testapi-4ea72-firebase-adminsdk-thkcf-6e888c94f2.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'testapi-4ea72.appspot.com'
})

bucket = storage.bucket()

blobs = bucket.list_blobs()

now = datetime.datetime.now(datetime.timezone.utc)
one_day_ago = now - datetime.timedelta(days=1)


for blob in blobs:

    if blob.time_created < one_day_ago:
        blob.delete()

print("Imagenes borradas en firebase")
