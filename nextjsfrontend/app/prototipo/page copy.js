"use client"
import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';
import QRCode from "react-qr-code";
import { Timer } from "./Timer.js"
import { Transition } from '@headlessui/react'

export default function Home() {
    const staticImageSrc = '/Rembrandt.jpg';
    const [imgSrc, setImageSrc] = useState(staticImageSrc)
    const websocketRef = useRef(null);
    const [isDetectingFace, setIsDetectingFace] = useState(false)
    const [showQRcode, setShowQRcode] = useState(false)
    const [imageURL, setImageURL] = useState("")
    const [isTimerOn, setIsTimerOn] = useState(false)
    const [isFlash, setIsFlash] = useState(false)
    const [progress, setProgress] = useState(0)
    const [isGeneratingAI, setIsGeneratingAI] = useState(false)
    const [iflag, setFlag] = useState(false)
    const [randomN, setRandomN] = useState(0)


    useEffect(() => {
        
        const websocket = new WebSocket('ws://localhost:8000/ws');
        websocketRef.current = websocket;
        
        websocket.onopen = () => {
            console.log("WebSocket connection established.");
        };

        websocket.onerror = (error) => {
          console.log("WebSocket error:", error);
        };

        websocket.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        websocket.onmessage = (event) => {
            const message = event.data

            if (message.startsWith('text_message')){

              const text_message = message.slice(13)
              

              if (text_message === 'No people detected') {
                
                setImageSrc(staticImageSrc);
                setIsDetectingFace(false)
                setShowQRcode(false)

              } else if (text_message.startsWith('image')) {
              
                const image_url = message.slice(10) 
                console.log(image_url)
                setImageURL(image_url)
                setShowQRcode(true)
              
              } else if (text_message === 'show counter') {

                setIsTimerOn(true)

              } else if (text_message === 'hide counter') {

                setIsTimerOn(false)

              } else if (text_message.startsWith('progress')) {

                const new_progress = Number(text_message.slice(9))
                setIsGeneratingAI(true)
                setProgress(new_progress)
                console.log(text_message.slice(9))
              }

            } else {

                const src = `data:image/jpeg;base64,${message}`;
                setImageSrc(src);
                setIsDetectingFace(true)
                setShowQRcode(false)
            } 

        };

        



        return () => {

                websocketRef.current.close();
            
        };
    }, []);


  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <Head>
        <title>Dark Chamber Rembrandt</title>
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

        {isTimerOn  ? 
          <Timer secondsToWait={5} setIsVisible={() => {
              setIsTimerOn(false)
              setIsFlash(true)
              setTimeout(() => {
                setIsFlash(false)
              }, "200");
              setTimeout(() => {
                setIsGeneratingAI(true)
              }, "300");

            }}/> : <></>}
          
          <Transition
            show={isFlash}
            enter="transition-opacity duration-0"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity duration-400"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed top-0 left-0 w-full h-full bg-white"></div>
          </Transition>
        

        {isGeneratingAI ? <div className="p-1 text-2xl font-bold w-1/2 fixed left-50 bottom-20 opacity-70">
          <h1 className="mb-4 text-center">Generando imagen {progress}%</h1>
          <div className="flex w-full rounded-full  border-white border-2 p-4">
            <div
              className="h-6 bg-gray-600 rounded-full dark:bg-gray-100"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div> : <></>}

      </main>
    </div>
  );
}
