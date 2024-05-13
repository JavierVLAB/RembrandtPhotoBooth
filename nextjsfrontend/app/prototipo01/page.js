"use client"
import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';

export default function Home() {
    const staticImageSrc = '/Rembrandt.jpg';
    const [imgSrc, setImageSrc] = useState(staticImageSrc);
    const websocketRef = useRef(null);

    useEffect(() => {
        
        const websocket = new WebSocket('ws://localhost:8000/ws');
        websocketRef.current = websocket;
        websocket.onopen = () => {
            console.log("WebSocket connection established.");
        };

        websocket.onmessage = (event) => {
            const message = event.data

            if (message === 'No people detected') {
                console.log("Received message:");
                setImageSrc(staticImageSrc);

            } else {

                const src = `data:image/jpeg;base64,${message}`;
                setImageSrc(src);
            }
        };

        websocket.onerror = (error) => {
            console.log("WebSocket error:", error);
        };

        websocket.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        return () => {
            if (websocketRef.current) {
                websocketRef.current.close();
            }
        };
    }, []);


  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <Head>
        <title>Imagen Centrada con Botones</title>
        <meta name="description" content="Web app con Next.js que muestra una imagen y botones" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex flex-1 flex-col items-center justify-center">
      <img src={imgSrc} alt="Webcam Stream" 
            style={{ width: "400", height: "600" }} />
      <div className="mt-5">
          <button className="mx-2 px-4 py-2 text-lg cursor-pointer">Boton 1</button>
          <button className="mx-2 px-4 py-2 text-lg cursor-pointer">Boton 2</button>
        </div>
      </main>
    </div>
  );
}
