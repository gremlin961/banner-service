# This web service uses FastAPI to accept requests for generated images using GCP's Imagen
#
# The following modules are used in this service
# fastapi - Web service framework used to build the API
# pydantic - Parsing library used to easily parse the provided json data to the API
# typing - Primarliy using the Union function to handle optional json data passed to the API
# GenImage - Custom library used to manage the generated AI images and layer them for the final banner

from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Union

from pkg import GenImage


# Define the parameters passed to the API and parsed uisng pydantic
class Item(BaseModel):
    project_id: str
    location: str
    imagen_prompt: str
    im_background_sz: str
    im_background_color: str 
    img_bucket: Union[str, None] = None
    img2_name: Union[str, None] = None
    img3_name: Union[str, None] = None 
    img1_pos: str
    img2_pos: Union[str, None] = None
    img3_pos: Union[str, None] = None


app = FastAPI()


# Define the entry point for the API 
@app.post("/items/", responses = {200:{"content":{"image/png":{}}}},response_class=Response)
async def create_item(item: Item):
    
    # Define the provided data and create a dictionary
    item_dict = item.dict()
    
    # Use the submit function in GenImage to generate the AI image
    generated_image = GenImage.submit(item.project_id,item.location,item.imagen_prompt)

    # Use the background function in GenImage to create a background image for the banner
    background = GenImage.background(item.im_background_sz, item.im_background_color)
    
    # If a second image will be added to the banner, download it from GCS and return it as a byte stream
    if item.img2_name:
        img2 = GenImage.GetImage(item.project_id, item.img_bucket, item.img2_name)
    else:
        img2 = 'FALSE'
        item.img2_pos = 'FALSE'

    # If a third image will be added to the banner, download it from GCS and return it as a byte stream
    if item.img3_name:
        img3 = GenImage.GetImage(item.project_id, item.img_bucket, item.img3_name)
    else:
        img3 = 'FALSE'
        item.img3_pos = 'FALSE'

    # Use the layer function in GenImage to create the final image and return it to the client
    final_image = GenImage.layer(background, generated_image, item.img1_pos, img2, item.img2_pos, img3, item.img3_pos)
    return Response(content=final_image, media_type="image/png")
