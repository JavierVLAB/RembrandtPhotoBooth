"use client"
import React, { useEffect, useState } from "react";

export const Flash = ({setIsVisible}) => {


  useEffect(() => {

    const timer = setTimeout(() => {
        setIsVisible()
    }, 3000);
    
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="fixed top-0 left-0 w-full h-full transition-opacity">
      <div className="fixed top-0 left-0 w-full h-full bg-white">

      </div>
    </div>
  );
};
