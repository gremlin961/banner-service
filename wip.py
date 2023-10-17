from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Union
from fastapi.responses import FileResponse

from pkg import GenImage


class Item(BaseModel):
    project_id: str
    location: str
    imagen_prompt: str
    im_background_sz: str
    im_background_color: str 
    img2_path: Union[str, None] = None
    img3_path: Union[str, None] = None 
    img1_pos: str
    img2_pos: Union[str, None] = None
    img3_pos: Union[str, None] = None


app = FastAPI()


#@app.post("/items/")
@app.post("/items/", responses = {200:{"content":{"image/png":{}}}},response_class=Response)
async def create_item(item: Item):
    item_dict = item.dict()
    #if item.img2_path:
        #do something
    generated_image = GenImage.submit(item.project_id,item.location,item.imagen_prompt)

    background = GenImage.background(item.im_background_sz, item.im_background_color)
    
    final_image = GenImage.layer(background, generated_image, item.img1_pos)
    return Response(content=final_image, media_type="image/png")
