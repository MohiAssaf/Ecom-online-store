import string
import random
from PIL import Image, ImageDraw, ImageFont


def generate_captcha_text():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



def generate_captcha_img(text):
    font = ImageFont.load_default(10)
    image = Image.new('RGB', (70, 25), color=(196, 164, 132))
    draw = ImageDraw.Draw(image)
    draw.text((10, 5), text, font=font, fill=(0, 0, 0))
    return image
    
    