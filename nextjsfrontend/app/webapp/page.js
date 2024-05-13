"use client"
import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';

export default function Home() {
    const [isStreaming, setIsStreaming] = useState(false);
    const imgRef = useRef(null);
    const websocketRef = useRef(null);

    const startStreaming = () => {
        if (!isStreaming) {
          // Crea una nueva conexión WebSocket al servidor de FastAPI
          const websocket = new WebSocket('ws://localhost:8000/ws');
          websocketRef.current = websocket;
    
          websocket.onopen = () => {
            console.log('WebSocket Connection Established');
          };
    
          websocket.onmessage = (event) => {
            // Crea una URL a partir del Blob recibido y actualiza el elemento img
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
    
          setIsStreaming(true);
        }
      };
    
      const stopStreaming = () => {
        if (websocketRef.current) {
          websocketRef.current.close();
          setIsStreaming(false);
        }
      };
    
      const handleTakePhoto = async () => {
        // Envía una solicitud para tomar una foto
        stopStreaming();
        const response = await fetch('http://localhost:8000/take-photo', { 
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }});
        const blob = await response.blob();
        if (imgRef.current) {
          imgRef.current.src = URL.createObjectURL(blob);
        }
      };

      const originalPhoto = async () => {
        // Envía una solicitud para tomar una foto
        stopStreaming();
        imgRef.current.src = "/Rembrandt.jpg";
        
      };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <Head>
        <title>Imagen Centrada con Botones</title>
        <meta name="description" content="Web app con Next.js que muestra una imagen y botones" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex flex-1 flex-col items-center justify-center">
      <img ref={imgRef} alt="Webcam Stream" 
            style={{ width: "400", height: "600" }} 
            src="/Rembrandt.jpg" />
      <div className="mt-5">
          <button className="mx-2 px-4 py-2 text-lg cursor-pointer" 
                    onClick={startStreaming} disabled={isStreaming}>Start Streaming</button>
          <button className="mx-2 px-4 py-2 text-lg cursor-pointer" 
                    onClick={stopStreaming} disabled={!isStreaming}>Stop Streaming</button>
          <button className="mx-2 px-4 py-2 text-lg cursor-pointer" 
                    onClick={handleTakePhoto}>Take Photo</button>
        <button className="mx-2 px-4 py-2 text-lg cursor-pointer" 
                    onClick={originalPhoto}>Rembrandt</button>
        </div>
      </main>
    </div>
  );
}
