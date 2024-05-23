import cv2

def insert_logos(background_image_path, output_image_path):
    # Rutas de las imágenes

    overlay_image_path = 'img_2.png'


    # Leer las imágenes
    background_image = cv2.imread(background_image_path)
    overlay_image = cv2.imread(overlay_image_path, cv2.IMREAD_UNCHANGED)

    if background_image is None:
        print(f"Error: No se pudo leer la imagen de fondo desde {background_image_path}")
        return

    if overlay_image is None:
        print(f"Error: No se pudo leer la imagen superpuesta desde {overlay_image_path}")
        return

    # Verificar que la imagen superpuesta tenga un canal alfa
    if overlay_image.shape[2] != 4:
        print("Error: La imagen superpuesta no tiene un canal alfa")
        return

    # Separar los canales de la imagen superpuesta
    overlay_b, overlay_g, overlay_r, overlay_a = cv2.split(overlay_image)
    overlay_rgb = cv2.merge((overlay_b, overlay_g, overlay_r))
    alpha_mask = overlay_a / 255.0

    # Combinar las imágenes usando la máscara alfa
    for c in range(0, 3):
        background_image[:, :, c] = (1. - alpha_mask) * background_image[:, :, c] + alpha_mask * overlay_rgb[:, :, c]

    # Guardar la imagen resultante
    cv2.imwrite(output_image_path, background_image)
    #print(f"Imagen guardada en {output_image_path}")


def mix_with_png(background_image, overlay_image_path):
    # Rutas de las imágenes

    overlay_image = cv2.imread(overlay_image_path, cv2.IMREAD_UNCHANGED)

    # Separar los canales de la imagen superpuesta
    overlay_b, overlay_g, overlay_r, overlay_a = cv2.split(overlay_image)
    overlay_rgb = cv2.merge((overlay_b, overlay_g, overlay_r))
    alpha_mask = overlay_a / 255.0

    # Combinar las imágenes usando la máscara alfa
    for c in range(0, 3):
        background_image[:, :, c] = (1. - alpha_mask) * background_image[:, :, c] + alpha_mask * overlay_rgb[:, :, c]

    return background_image

if __name__ == "__main__":
    insert_logos('test_scripts/imagen_1.png', 'images_out/combined_image.png')
