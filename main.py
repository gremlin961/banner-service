from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Union

from pkg import GenImage


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


#@app.post("/items/")
@app.post("/items/", responses = {200:{"content":{"image/png":{}}}},response_class=Response)
async def create_item(item: Item):
    item_dict = item.dict()
    
    generated_image = GenImage.submit(item.project_id,item.location,item.imagen_prompt)

    background = GenImage.background(item.im_background_sz, item.im_background_color)
    
    if item.img2_name:
        img2 = GenImage.GetImage(item.project_id, item.img_bucket, item.img2_name)
    else:
        img2 = 'FALSE'
        item.img2_pos = 'FALSE'

    if item.img3_name:
        img3 = GenImage.GetImage(item.project_id, item.img_bucket, item.img3_name)
    else:
        img3 = 'FALSE'
        item.img3_pos = 'FALSE'

    final_image = GenImage.layer(background, generated_image, item.img1_pos, img2, item.img2_pos, img3, item.img3_pos)
    return Response(content=final_image, media_type="image/png")
