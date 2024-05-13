"use client"
import React, { useEffect, useRef, useState } from 'react';

function VideoStreamComponent() {
    const staticImageSrc = '/Rembrandt.jpg';
    const [imageSrc, setImageSrc] = useState(staticImageSrc);
    const [textToShow, setTextToShow] = useState("hola")
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
                setTextToShow("Xssss")
            } else {
                console.log("Received image");
                setTextToShow("sssss")
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
        <div>
            <img src={imageSrc} alt="Camera Feed" />
            <button className="mx-2 px-4 py-2 text-lg cursor-pointer" 
                    >{textToShow}</button>
        </div>
    );
}

export default VideoStreamComponent;

