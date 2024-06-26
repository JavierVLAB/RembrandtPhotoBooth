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
      // funcion que maneja los mensajes recibidos por websocket
      const message = event.data

      setMsgCount(msgCount+1)
      
      if (message.startsWith('text_message')){
        // Se recibe con todos los mensajes que no son una imagen
        const text_message = message.slice(13)
        //console.log(text_message)

        if (text_message === 'No people detected') {
          // Cuando no se detecta a nadie
          setImageSrc(staticImageSrc);
          setIsDetectingFace(false)
          setShowQRcode(false)
          setShowEyeArea(false)


        } else if (text_message.startsWith('image')) {
          //cuando se recibe el nombre de la imagen para generar el qrcode
          const image_url = text_message.slice(10) 
          console.log(image_url)
          setImageURL(image_url)
          
          setShowQRcode(true)
          setIsGeneratingAI(false)
          setShowEyeArea(false)
        
        } else if (text_message === 'show counter') {
          // Cuando la persona esta colocada correctamente
          //y se empieza a contar antes de la fot
          setIsTimerOn(true)
          setProgress(0)
          setShowEyeArea(false)

        } else if (text_message === 'hide counter') {
          // cuando la persona se sale de la posicion correcta
          setIsTimerOn(false)
          setShowEyeArea(true)

        } else if (text_message.startsWith('progress')) {
          //cuando comfyui esta generando la imagen
          const new_progress = Math.round(Number(text_message.slice(9))*100)
          setIsGeneratingAI(true)
          setProgress(new_progress)
          setShowEyeArea(false)
          //console.log(new_progress)
          //setImageSrc(staticImageSrc);
        }

      } else {
          //cuando se recibe una imagen
          const src = `data:image/jpeg;base64,${message}`;
          setImageSrc(src);
          setIsDetectingFace(true)
          setShowQRcode(false)
          setShowEyeArea(true)
      }
    }, [])   


    useEffect(() => {
      //funciones para websocket

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
          <Image // muestra la imagen principal
            src={imgSrc}
            alt="Imagen recibida por websocket"
            width={756} // Especifica el ancho deseado
            height={945} // Especifica la altura deseada
            style={{ objectFit: 'cover' }} // Esto asegura que la imagen se escale correctamente
          />
            {// muestra el recuadro donde hay que poner los ojos
            (showEyeArea & !isTimerOn) ? <div className="absolute inset-0 flex justify-center">
              
              <div className="absolute top-1/4 bg-white bg-opacity-40 w-[300px] h-[300px] rounded-lg items-center justify-center">
              {/*<h1 className="mb-4 text-[50px] tex-black opacity-50">Zona para ojos</h1>*/}
              </div>
            </div> : <></>}

            { showQRcode ?
              // 
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
        //muestra el contador de tiempo antes de tomar la foto
        <div className='absolute justify-center bottom-40'>
          <Timer secondsToWait={time_before_foto} setIsVisible={() => {
              setIsTimerOn(false)
              setIsFlash(true)
              setShowEyeArea(false)
              setTimeout(() => {
                setIsFlash(false)
              }, "200");


            }}/> </div>: <></>}
          
          {/* muestra el div blanco que simula el flash*/}
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
          //muestra la barra de progreso 
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
