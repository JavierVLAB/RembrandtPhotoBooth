::Clean local Images
del C:\Users\User\RembrandtPhotoBooth\backend\images\img*
del C:\Users\User\RembrandtPhotoBooth\backend\images_out\img*

::Clean Cloud Images
cd C:\Users\User\RembrandtPhotoBooth\backend
call venv\Scripts\activate
python firebase_clean.py
exit