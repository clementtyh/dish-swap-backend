from fastapi import HTTPException, APIRouter, Depends
from services.auth_services import validate_token
import cloudinary
import cloudinary.uploader
import os
import json
import time
import re
import requests
from utils.validator import validate_file_size

router = APIRouter()

cloudinary_config_path = os.environ.get("CLOUDINARY_CONFIG_JSON")

with open(cloudinary_config_path, "r") as config_file:
    cloudinary_config = json.load(config_file)

cloudinary.config(
    cloud_name=cloudinary_config["cloud_name"],
    api_key=cloudinary_config["api_key"],
    api_secret=cloudinary_config["api_secret"]
)

@router.post("/upload_params") 
async def get_upload_url(user_id: str = Depends(validate_token)): 
    try: 
        upload_preset = "ml_default" 
        timestamp = int(time.time()) + 600 
        signature = cloudinary.utils.api_sign_request( 
            {"upload_preset": upload_preset, "timestamp": timestamp}, 
            cloudinary.config().api_secret 
        ) 
 
        return {"timestamp": timestamp, "upload_preset": upload_preset, "signature": signature} 
     
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    

def is_valid_cloudinary_image(image_url):
    if not image_url:
        return False
    
    public_id_match = re.search(r'/v\d+/(.*?)(\.\w+)?$', image_url)
    public_id = public_id_match.group(1) if public_id_match else None

    if public_id:
        cloudinary_url = cloudinary.utils.cloudinary_url(public_id)[0]
    
        try:
            response = requests.get(cloudinary_url, stream=True)
            if response.status_code == 200:
                content_length = int(response.headers.get("Content-Length"))
                if not validate_file_size(content_length): 
                    return False
                else:
                    return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
    return False

async def delete_cloudinary_images(image_urls):
    try:
        for image_url in image_urls:
            public_id = await extract_public_id(image_url)
            folder_path = await extract_folder_path(image_url)

            result = cloudinary.uploader.destroy(folder_path+public_id)
            if result.get("result") == "ok":
                print(f"Deleted image: {image_url}")
            else:
                print(f"Failed to delete image: {image_url}")
                return False
        return True
    except Exception as e:
        print(f"Error deleting images: {str(e)}")

async def extract_public_id(image_url):
    parts = image_url.split("/")
    return parts[-1].split(".")[0]

async def extract_folder_path(image_url):
    parts = image_url.split("/")
    return parts[-2]+"/"