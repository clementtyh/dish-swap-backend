import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
from models.response import ErrorOut
from typing import List
import os
import json

cloudinary_config_path = os.environ.get("CLOUDINARY_CONFIG_JSON")

with open(cloudinary_config_path, "r") as config_file:
    cloudinary_config = json.load(config_file)

cloudinary.config(
    cloud_name=cloudinary_config["cloud_name"],
    api_key=cloudinary_config["api_key"],
    api_secret=cloudinary_config["api_secret"]
)

def upload_image_files_to_cloud(image_files: List[UploadFile]):
    try:
        file_urls = []
        for file in image_files:
            result = cloudinary.uploader.upload(file, folder="dishswap")
            file_urls.append(result["url"])
    
        return file_urls
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())