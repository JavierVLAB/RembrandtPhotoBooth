# Upload an image to the firebase storage
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('auth/testapi-4ea72-firebase-adminsdk-thkcf-6e888c94f2.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'testapi-4ea72.appspot.com'
})


def upload_image_to_firebase(file_path, destination_blob_name):
    """Sube una imagen a Firebase Storage y retorna la URL pública"""
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)

    # Sube el archivo
    blob.upload_from_filename(file_path)

    # Hacer que el archivo sea de acceso público
    blob.make_public()

    # Retorna la URL pública
    return blob.public_url

if __name__ == "__main__":
    file_path = 'images/testJavi01.jpg'  #local image
    destination_blob_name = 'imagenes/imagetest03.jpg'  #image path in the cloud storage
    
    public_url = upload_image_to_firebase(file_path, destination_blob_name)
    print(f"Archivo subido a {public_url}")
