
import easyocr
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()


def IMG_TO_TEXT(path: str):
    reader = easyocr.Reader(['ch_sim', 'en']) # this needs to run only once to load the model into memory

    result=reader.readtext(path)
    text=''
    for i in range(len(result)):
        text=text + result[i][1]
    return text
    
# reader = easyocr.Reader(['ch_sim', 'en', 'fr', 'de', 'es', 'ru',f'{os.getenv("LANGUAGE")}']) # this needs to run only once to load the model into memory
# result = reader.readtext(r"C:\Users\z0052mvs\Pictures\Screenshots\Screenshot 2025-08-13 152426.png")

# # print(result)
# for i in range(len(result)):
#     print(result[i][1],end=" ")