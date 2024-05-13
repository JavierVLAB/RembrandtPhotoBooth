import { useEffect, useRef } from 'react';

function Home() {
  const imgRef = useRef(null);

  useEffect(() => {
    // Crear una nueva conexión WebSocket al servidor de FastAPI
    const websocket = new WebSocket('ws://localhost:8000/ws');

    websocket.onopen = () => {
      console.log('WebSocket Connection Established');
    };

    websocket.onmessage = (event) => {
      // Convertir el Blob de datos en una URL y actualizar la imagen
      const blob = new Blob([event.data]);
      const url = URL.createObjectURL(blob);
      if (imgRef.current) {
        imgRef.current.src = url;
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket Connection Closed');
    };

    // Limpiar la conexión al desmontar el componente
    return () => {
      websocket.close();
    };
  }, []);

  const handleTakePhoto = async () => {
    // Envía una solicitud para tomar una foto
    const response = await fetch('http://localhost:8000/take-photo', { method: 'POST' });
    const blob = await response.blob();
    if (imgRef.current) {
      imgRef.current.src = URL.createObjectURL(blob);
    }
  };

  return (
    <div>
      <img ref={imgRef} alt="Webcam Stream" />
      <button onClick={handleTakePhoto}>Take Photo</button>
    </div>
  );
}

export default Home;

