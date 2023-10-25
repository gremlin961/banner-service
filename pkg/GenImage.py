import vertexai
from vertexai.preview.vision_models import Image, ImageGenerationModel
from PIL import Image
from io import BytesIO
from os import remove
from google.cloud import storage 


def submit(PROJECT_ID, LOCATION, PROMPT):
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    model = ImageGenerationModel.from_pretrained("imagegeneration@002")
    image = model.generate_images(
        prompt=PROMPT,
        number_of_images=1
    )
    image[0].save(location="./gen-img1.png", include_generation_parameters=False)
    image_tmp = "./gen-img1.png"
    image1 = Image.open(image_tmp).convert("RGBA")
    buf = BytesIO()
    image1.save(buf, 'PNG')
    remove(image_tmp)
    return image1


def background(SIZE, COLOR):
    size = eval(SIZE)
    color = eval(COLOR)
    im_background = Image.new(mode = "RGBA", size = (size), color = (color))
    return im_background


def GetImage(PROJECT_ID, BUCKET, FILE):
    storage_client = storage.Client(PROJECT_ID)
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(FILE)
    result = blob.download_as_bytes()
    return result


def layer(BACKGROUND, IMAGE1, IMAGE1_POSITION, IMAGE2='FALSE', IMAGE2_POSITION='FALSE', IMAGE3='FALSE', IMAGE3_POSITION='FALSE', BANNER_SIZE):
    image1_pos = eval(IMAGE1_POSITION)
    image0 = BACKGROUND
    image1 = IMAGE1
    image0.paste(image1, image1_pos, mask = image1)
    if IMAGE2 != 'FALSE':
        image2_data = IMAGE2
        image2_pos = eval(IMAGE2_POSITION)
        image2 = Image.open(BytesIO(image2_data)).convert("RGBA")        
        image0.paste(image2, image2_pos, mask = image2)
    if IMAGE3 != 'FALSE':
        image3_data = IMAGE3
        image3_pos = eval(IMAGE3_POSITION)        
        image3 = Image.open(BytesIO(image3_data)).convert("RGBA")
        image0.paste(image3, image3_pos, mask = image3)
    #image0 = image0.resize((468, 60))
    image0 = image0.resize((BANNER_SIZE))
    image0.convert('RGB')    
    buf = BytesIO()
    image0.save(buf, format='PNG')
    result = buf.getvalue()
    return result