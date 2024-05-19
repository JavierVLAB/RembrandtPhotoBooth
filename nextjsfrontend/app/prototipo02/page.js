"use client"
import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';
import QRCode from "react-qr-code";

export default function Home() {
    const staticImageSrc = '/Rembrandt.jpg';
    const [imgSrc, setImageSrc] = useState(staticImageSrc);
    const websocketRef = useRef(null);
    const [isDetectingFace, setIsDetectingFace] = useState(false)
    const [showQRcode, setShowQRcode] = useState(false)
    const [imageURL, setImageURL] = useState("")

    useEffect(() => {
        
        const websocket = new WebSocket('ws://localhost:8000/ws');
        websocketRef.current = websocket;
        websocket.onopen = () => {
            console.log("WebSocket connection established.");
        };

        websocket.onmessage = (event) => {
            const message = event.data

            if (message === 'No people detected') {
                
                setImageSrc(staticImageSrc);
                setIsDetectingFace(false)
                setShowQRcode(false)

            } else if (message.startsWith('image')) {
              
              const image_url = message.slice(10) 
              console.log(image_url)
              setImageURL(image_url)
              setShowQRcode(true)

            } else {

                const src = `data:image/jpeg;base64,${message}`;
                setImageSrc(src);
                setIsDetectingFace(true)
                setShowQRcode(false)
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
              style={isDetectingFace ? { width: "50%"} : { width: "40%"} } />

        
        
        { showQRcode ?
          <div className="p-6 bg-white rounded-xl fixed left-50 bottom-10">
            <QRCode
                size={200}
                style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                value={imageURL}
                viewBox={`0 0 200 200`}
                /> 
          </div> : <></>
        }
         
      </main>
    </div>
  );
}
