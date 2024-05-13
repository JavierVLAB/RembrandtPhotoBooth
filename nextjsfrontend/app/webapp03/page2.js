import { useEffect, useState } from 'react';

function VideoStreamComponent() {
    const [imageSrc, setImageSrc] = useState('/static-image.jpg'); // Imagen inicial
    const [ws, setWs] = useState(null);

    useEffect(() => {
        // Inicializar la conexión WebSocket al montar el componente
        const websocket = new WebSocket('ws://localhost:8000/ws');
        websocket.onmessage = (event) => {
            if (event.data === 'No people detected') {
                setImageSrc('/static-image.jpg'); // Cambiar de nuevo a la imagen estática
            } else {
                // Asumiendo que los datos son un blob de imagen cuando hay detección
                const blob = new Blob([event.data], { type: 'image/jpeg' });
                const url = URL.createObjectURL(blob);
                setImageSrc(url); // Mostrar el frame del video
            }
        };
        setWs(websocket);

        return () => {
            // Cerrar la conexión WebSocket al desmontar el componente
            websocket.close();
        };
    }, []);

    return (
        <div>
            <img src={imageSrc} alt="Camera Feed" />
        </div>
    );
}

export default VideoStreamComponent;
