from fastapi import HTTPException
from utils.validator import validate_file_size
import cloudinary
import cloudinary.uploader
import re
import requests
from utils.logger import logger
from models.response import ErrorOut


class FileServices():

    def is_valid_cloudinary_image(self, image_url):
        try:
            if not image_url:
                return False
            
            public_id_match = re.search(r'/v\d+/(.*?)(\.\w+)?$', image_url)
            public_id = public_id_match.group(1) if public_id_match else None

            if public_id:
                cloudinary_url = cloudinary.utils.cloudinary_url(public_id)[0]
            
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
            logger.error(e)
            return False


    async def delete_cloudinary_images(self, image_urls):
        try:
            for image_url in image_urls:
                image_path = await self.extract_image_path(image_url)

                if image_path is not None:
                    result = cloudinary.uploader.destroy(image_path)
                    if result.get("result") != "ok":
                        return False
                else:
                    return False
            return True
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())


    async def extract_image_path(self, image_url):
        parts = image_url.split('/')

        version_index = -1
        for i, part in enumerate(parts):
            if part.startswith('v'):
                version_index = i
                break

        if version_index == -1:
            return None

        if version_index + 1 < len(parts):
            image_path = '/'.join(parts[version_index + 1:])
            image_path = image_path.split(".")[0]
            return image_path
        else:
            return parts[-1].split(".")[0]