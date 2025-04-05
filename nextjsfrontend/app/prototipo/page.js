"use client"
import Image from 'next/image';
import Head from 'next/head';
import { useEffect, useRef, useState, useCallback } from 'react';
import QRCode from "react-qr-code";
import { Timer } from "./Timer.js"
import { Transition } from '@headlessui/react'
import './style.css'
import toast, { Toaster } from 'react-hot-toast';

export default function Home() {
    const staticImageSrc = '/Rembrandt.jpg';
    const [imgSrc, setImageSrc] = useState(staticImageSrc)
    const [imgPngSrc, setImagePngSrc] = useState('/img.png')
    const websocketRef = useRef(null);
    const [imageURL, setImageURL] = useState("")
    const [isFlash, setIsFlash] = useState(false)
    const [progress, setProgress] = useState(0)

    const [msgCount, setMsgCount] = useState(0)

    const [selectedDiv, setSelectedDiv] = useState('')

    const [background_img, setBackground] = useState('Fondo_DC_01.jpg')

    const [firstConnection, setFirstConnection] = useState(false)

    const requestRef = useRef(null);
    
    const time_before_foto = 5
    const time_QR_code = 20

    const bg_img_url_style = {
      backgroundImage: `url(/${background_img})`
    } 
    
    const handleWebSocketMessages = useCallback((event) => {
      // funcion que maneja los mensajes recibidos por websocket
      const message = event.data

      setMsgCount(msgCount+1)

      if (typeof message === 'string') {
      
        if (message.startsWith('text_message')){
          // Se recibe con todos los mensajes que no son una imagen
          const text_message = message.slice(13)
          //console.log(text_message)

          if (text_message === 'No people detected') {
            // Cuando no se detecta a nadie
            setImageSrc(staticImageSrc);
            setSelectedDiv('')

            setBackground('Fondo_DC_01.jpg')


          } else if (text_message.startsWith('image')) {
            //cuando se recibe el nombre de la imagen para generar el qrcode
            const image_url = text_message.slice(10) 
            //console.log(image_url)
            setImageURL(image_url)

            setSelectedDiv('showQRCode')
            setBackground('Fondo_DC_04.jpg')

          
          } else if (text_message === 'show counter') {
            // Cuando la persona esta colocada correctamente
            //y se empieza a contar antes de la fot

            setSelectedDiv('showTimer')
            //setBackground('Fondo_DC_01.jpg')

          
          } else if (text_message === 'hide QR') {
            // Cuando la persona esta colocada correctamente
            //y se empieza a contar antes de la fot

            setSelectedDiv('')


          } else if (text_message === 'hide counter') {
            // cuando la persona se sale de la posicion correcta
            
            setSelectedDiv('showfaceArea')


          } else if (text_message === 'show wait screen') {
            // cuando la persona se sale de la posicion correcta
            setBackground('Fondo_DC_03.jpg')


          } else if (text_message.startsWith('progress')) {
            //cuando comfyui esta generando la imagen
            const new_progress = Math.round(Number(text_message.slice(9))*100)
            setProgress(new_progress)
            setSelectedDiv('showProgress')

          } else if (text_message.startsWith('reload')) {
            //cuando comfyui esta generando la imagen
            setTimeout(()=> {
              window.location.reload()
            },500)

          }
        }
      } else if (message instanceof ArrayBuffer){
          //cuando se recibe una imagen

            const blob = new Blob([event.data], { type: 'image/jpeg' });
            const url = URL.createObjectURL(blob);
            setImageSrc(url);

          setBackground('Fondo_DC_02.jpg')
      }
    }, [])   


    useEffect(() => {
      
      // Queremos que se recague en 30 minutos
      const timeout = setTimeout(() => {
        console.log('Reiniciando')
        window.location.reload();
      }, 30 * 60 * 1000);

      //funciones para websocket

      const websocket = new WebSocket('ws://localhost:8000/ws');
      websocketRef.current = websocket;
      websocket.binaryType = 'arraybuffer';
      
      websocket.onopen = () => {
          console.log("WebSocket connection established.");
          toast.success('Server ready!')
          setFirstConnection(true)
      };

      websocket.onerror = (error) => {
        console.log("WebSocket error:", error);
      };

      websocket.onclose = () => {
          console.log("WebSocket connection closed.");
          if (firstConnection) {
            window.location.reload()
          }
      }; 

      websocket.onmessage = handleWebSocketMessages

      return () => {

        clearTimeout(timeout)

        if (websocketRef.current) {
          websocketRef.current.close();
        }
        if (requestRef.current) {
          cancelAnimationFrame(requestRef.current);
        }
      };

    }, [handleWebSocketMessages]);

    const renderContent = () => {
      //console.log(selectedDiv)
      
      switch (selectedDiv) {
      //switch ('showQRCode') {
        case 'showfaceArea':
          return (
            <div className="absolute inset-0 flex justify-center">
              <div className="absolute top-1/4  w-[400px] h-[400px] rounded-lg items-center justify-center">
                <img className="text-white bg-opacity-40" src="/face-area.svg"></img>
              </div>
            </div>
          )

        case 'showTimer':
          return (
            <div className='absolute justify-center bottom-40'>
              <Timer secondsToWait={time_before_foto} size={'200px'}
                  shootflash={() =>
                    setSelectedDiv('showFlash')
                  }
                  setIsVisible={() => {

                    setIsFlash(true)
                    setImagePngSrc('/img.png')
                    setTimeout(() => {
                      setIsFlash(false)
                  }, "200");
                }}/> </div>
          )

        case 'showQRCode':
          return (
            <div className='fixed left-50 top-[1440px] text-center'>
              <div className=" shadow-2xl pt-6 px-6 pb-3 bg-white rounded-xl  ">
                <QRCode
                  size={200}
                  style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                  value={imageURL}
                  viewBox={`0 0 200 200`}
                /> 
                <div className="font-bold text-black text-[30px]">#Artvivant2024</div>
              </div>

              <Timer secondsToWait={time_QR_code} className="justify-center" size={'100px'}
                      setIsVisible={()=>{}} shootflash={() => {}}/> 
            </div>
          )

        case 'showProgress':
          return (
            <div className="absolute p-1 text-2xl font-bold w-3/4 fixed bottom-40 opacity-70 text-white">
              <h1 className="mb-4 text-center">Generando imagen {progress}%</h1>
              <div className="flex w-full rounded-full  border-white border-2 p-1">
                <div
                  className="h-6 bg-gray-600 rounded-full dark:bg-gray-100"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          )

        case 'showFlash':
          return (
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
          )

          default:
            return (<div></div>)

      }

    }



  return (
    <div className='flex min-h-screen flex-col items-center justify-center background' style={bg_img_url_style}>
      <Head>
        <title>Dark Chamber Rembrandt</title>
      </Head>

      <main className="flex flex-1 flex-col items-center justify-center">
       { /*
        <Image // muestra la imagen principal
            src={'/bg01.jpg'}
            priority={true}
            alt="Imagen de fondo"
            width={1200} // Especifica el ancho deseado
            height={1920} // Especifica la altura deseada
            //style={{ objectFit: 'cover' }} // Esto asegura que la imagen se escale correctamente
            className='fixed'
          />
        */}
        <div className='relative w-[756px] h-auto flex justify-center'>
        
          {/*<Image // muestra la imagen principal
            src={imgSrc}
            priority={true}
            alt="Imagen recibida por websocket"
            width={756} // Especifica el ancho deseado
            height={945} // Especifica la altura deseada
            style={{ objectFit: 'cover' }} // Esto asegura que la imagen se escale correctamente
            className=''
      />*/}

          <img 
            className="w-full fixed"
            src={imgSrc}
            alt="Imagen de fondo" 
            width="756" 
            height="945" 
            style={{ objectFit: 'cover' }}
          />

          {renderContent()}
        
        </div>

        <div><Toaster position="top-center" /></div>

      </main>

    </div>
  );
}
