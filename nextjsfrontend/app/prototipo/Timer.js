"use client"
import React, { useEffect, useState } from "react";

export const Timer = ({setIsVisible, secondsToWait, shootflash, size}) => {

  const [secs, setSecs] = useState(secondsToWait);

  useEffect(() => {

    let interval = setInterval(() => {

      var s = secs - 1;
      setSecs(s);

      if(s==0) {
        setIsVisible()
        shootflash()
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [secs]);

  return (
    <div className={`font-black text-white text-opacity-60`} style={{fontSize: size}}>
      {secs}
    </div>
  );
};
