from fastapi import HTTPException, APIRouter, Depends
from utils.logger import logger
from services.auth_services import AuthenticationServices
from models.response import ErrorOut
import cloudinary
import cloudinary.uploader
import os
import json
import time


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
async def get_upload_url(user_id: str = Depends(AuthenticationServices().validate_token)): 
    try: 
        upload_preset = "ml_default" 
        timestamp = int(time.time()) + 600 
        signature = cloudinary.utils.api_sign_request( 
            {"upload_preset": upload_preset, "timestamp": timestamp}, 
            cloudinary.config().api_secret 
        ) 
 
        return {"timestamp": timestamp, "upload_preset": upload_preset, "signature": signature} 
     
    except Exception as e: 
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
