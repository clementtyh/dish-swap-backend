import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
from models.response import ErrorOut
from typing import List

cloudinary.config(
    cloud_name='dishswap',
    api_key='542941728215527',
    api_secret='fOAsjq5kByGalJBEwj0HFfQMr-c')

def get_file_url(image_files: List[UploadFile]):
    try:
        file_urls = []
        for file in image_files:
            result = cloudinary.uploader.upload(file, folder="dishswap")
            file_urls.append(result["url"])
    
        return file_urls
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())