"use client"
import Image from 'next/image';
import Head from 'next/head';
import { useEffect, useRef, useState, useCallback } from 'react';
import QRCode from "react-qr-code";
import { Timer } from "./Timer.js"
import { Transition } from '@headlessui/react'
import './style.css'

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
    const [msgCount, setMsgCount] = useState(0)
    const [showEyeArea, setShowEyeArea] = useState(false)

    const time_before_foto = 3

    const handleWebSocketMessages = useCallback((event) => {

            const message = event.data

            setMsgCount(msgCount+1)
            
            if (message.startsWith('text_message')){

              const text_message = message.slice(13)
              

              if (text_message === 'No people detected') {
                
                setImageSrc(staticImageSrc);
                setIsDetectingFace(false)
                setShowQRcode(false)
                setShowEyeArea(false)


              } else if (text_message.startsWith('image')) {
              
                const image_url = text_message.slice(10) 
                console.log(image_url)
                setImageURL(image_url)
                
                setShowQRcode(true)
                setIsGeneratingAI(false)
                setShowEyeArea(false)
              
              } else if (text_message === 'show counter') {

                setIsTimerOn(true)
                setProgress(0)
                setShowEyeArea(false)

              } else if (text_message === 'hide counter') {

                setIsTimerOn(false)
                setShowEyeArea(true)

              } else if (text_message.startsWith('progress')) {

                const new_progress = Math.round(Number(text_message.slice(9))*100)
                setIsGeneratingAI(true)
                setProgress(new_progress)
                setShowEyeArea(false)
                //console.log(new_progress)
                //setImageSrc(staticImageSrc);
              }

            } else {

                const src = `data:image/jpeg;base64,${message}`;
                setImageSrc(src);
                setIsDetectingFace(true)
                setShowQRcode(false)
                setShowEyeArea(true)
            }
          }, [])   


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

        websocket.onmessage = handleWebSocketMessages

    
        return () => {

          websocketRef.current.close();
        };

    }, [handleWebSocketMessages]);



  return (
    <div className="flex min-h-screen flex-col items-center justify-center background">
      <Head>
        <title>Dark Chamber Rembrandt</title>
      </Head>

      <main className="flex flex-1 flex-col items-center justify-center">

        <div className='relative w-[756] h-945 flex justify-center'>
          <Image
            src={imgSrc}
            alt="Imagen recibida por websocket"
            width={756} // Especifica el ancho deseado
            height={945} // Especifica la altura deseada
            style={{ objectFit: 'cover' }} // Esto asegura que la imagen se escale correctamente
          />
            {(showEyeArea & !isTimerOn) ? <div className="absolute inset-0 flex justify-center">
              <div className="absolute top-1/4 bg-black bg-opacity-50 w-[300px] h-[300px] rounded-lg items-center">
              {/*<h1 className="mb-4 text-center">Zona para ojos</h1>*/}
              </div>
            </div> : <></>}

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
        <div className='absolute justify-center bottom-40'>
          <Timer secondsToWait={time_before_foto} setIsVisible={() => {
              setIsTimerOn(false)
              setIsFlash(true)
              setShowEyeArea(false)
              setTimeout(() => {
                setIsFlash(false)
              }, "200");
              setTimeout(() => {
                setIsGeneratingAI(true)
                
              }, "300");

            }}/> </div>: <></>}
          
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
        

        {isGeneratingAI ? 
          <div className="absolute p-1 text-2xl font-bold w-3/4 fixed bottom-40 opacity-70 text-white">
            <h1 className="mb-4 text-center">Generando imagen {progress}%</h1>
            <div className="flex w-full rounded-full  border-white border-2 p-1">
              <div
                className="h-6 bg-gray-600 rounded-full dark:bg-gray-100"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div> : <></>}
        
        </div>

        




      </main>

    </div>
  );
}
