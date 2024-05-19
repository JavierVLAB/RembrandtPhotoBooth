"use client"
import React, { useEffect, useState } from "react";

export const Timer = ({setIsVisible, secondsToWait}) => {

  const [secs, setSecs] = useState(secondsToWait);

  useEffect(() => {

    let interval = setInterval(() => {

      var s = secs - 1;
      setSecs(s);

      if(s==0) {
        setIsVisible()
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [secs]);

  return (
    <div className="justify-center fixed left-50 bottom-40 font-black text-9xl text-white text-opacity-60">
      {secs}
    </div>
  );
};
