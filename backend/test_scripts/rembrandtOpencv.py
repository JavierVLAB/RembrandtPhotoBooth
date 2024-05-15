import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

def apply_rembrandt_effect(img):
    # Cargar imagen
    
    
    if img is None:
        print("Error: no se pudo cargar la imagen.")
        return

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # equalized = cv2.equalizeHist(img)

    # blurred = cv2.GaussianBlur(equalized, (9, 9), 0)
    
    # alpha = 0.6
    # blended = cv2.addWeighted(equalized, alpha, blurred, 1 - alpha, 0)

    img2 = cv2.convertScaleAbs(img, alpha= 0.9, beta= -10)
    img2 = adjust_gamma(img2, gamma=1.0)
    esp = 500
    # Aplicar un efecto de viñeteado
    rows, cols = img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols,esp)
    kernel_y = cv2.getGaussianKernel(rows,esp)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    vignette = np.dstack([mask, mask, mask])


    rembrandt = np.uint8(img2 * vignette * 3)

    return rembrandt
    #rembrandt = np.uint8(img * vignette )

    # # Mostrar la imagen original y la modificada
    # cv2.imshow('Original', img)
    # cv2.imshow('Original2', img2)
    # cv2.imshow('Rembrandt Style', rembrandt)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# Cambia 'path_to_your_image.jpg' al path de tu imagen
#apply_rembrandt_effect('images/testJavi01.jpg')

