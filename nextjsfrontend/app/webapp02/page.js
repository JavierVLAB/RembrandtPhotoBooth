"use client"
import { useEffect, useState, useRef } from 'react';

function VideoStreamComponent() {
    const staticImageSrc = "/Rembrandt.jpg"
    const imageRef = useRef(null); // Referencia al elemento img

    useEffect(() => {
        // Inicializar la conexión WebSocket al montar el componente
        const websocket = new WebSocket('ws://localhost:8000/ws');
        
        websocket.onmessage = (event) => {
            if (event.data == 'No people detected') {
                if (imageRef.current) {
                    imageRef.current.src = staticImageSrc; // Asignar directamente la imagen estática
                }
            } else {
                const blob = new Blob([event.data], { type: 'image/jpeg' });
                const url = URL.createObjectURL(blob);
                if (imageRef.current) {
                    imageRef.current.src = url; // Asignar directamente el stream de video
                }
            }
        };

        return () => {
            // Cerrar la conexión WebSocket al desmontar el componente
            websocket.close();
        };
    }, []);

    return (
        <div>
            <img ref={imageRef} src={staticImageSrc} alt="Camera Feed" />           
        </div>
    );
}

export default VideoStreamComponent;
