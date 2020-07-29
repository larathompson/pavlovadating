
// //  cloudinary stuff
// import ReactFilestack from 'filestack-react'

import React, { useState, useEffect } from 'react'
import { CloudinaryContext, Image } from 'cloudinary-react'
import { fetchPhotos, openUploadWidget } from '../CloudinaryService'
import axios from 'axios'
// import './App.css'

function Images() {
  const [images, setImages] = useState('')
  console.log(images)

  const beginUpload = tag => {
    const uploadOptions = {
      cloudName: 'pavlova',
      tags: [tag],
      uploadPreset: 'upload'
    }

    openUploadWidget(uploadOptions, (error, photos) => {
      if (!error) {
        console.log(photos)
        if (photos.event === 'success') {
          console.log('hello', photos.info.secure_url)
          setImages(photos.info.secure_url)
        }
      } else {
        console.log(error)
      }
    })
  }
  //this fetches your pics from clouinary lib
  useEffect(() => {
    fetchPhotos('image', setImages)
  }, [])

  // function handleImage(res) {
  //   console.log('hello', res)

  // }

  useEffect(() => {
    axios.put('/api/preferences/user', { image_1: images })
     .then()
     console.log('you have posted')

  }, [images])

  // this images compoennts is meant to deliver them as source links which can then just be put in img tag

  return (
    <CloudinaryContext cloudName="pavlova">
      <div className="Images">
        <section> 
        <img src={images} alt='' />
          {/* {images.map((i, index) => <Image
            key={i}
            className={index}
            publicId={i}
            fetch-format="auto"
            quality="auto"
          />)} */}
          {/* /* {images.map((i,index) => <img src={i} alt='' key={index} />)} */}
        </section>
      </div>
      <button onClick={() => beginUpload()}> Upload Image </button>
    </CloudinaryContext >
  )
}
export default Images

