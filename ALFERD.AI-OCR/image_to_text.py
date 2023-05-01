
# PYTHON-ORC TESSARACT

# from PIL import Image
# import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# img = Image.open('./images/img4.png')
# text = tess.image_to_string(img)

# print(text) 



################################################################################################

#ORC-SPACE x Pytesseract



import requests
from PIL import Image
import pytesseract as tess
import http
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
api_key = 'K86847055688957'
image_path = '.\images\img2.png'

# Send a POST request to OCR.Space API with the image file and API key
response = requests.post('https://api.ocr.space/parse/image',
                         files={'image': open(image_path, 'rb')},
                         data={'apikey': api_key})

# Parse the JSON response and extract the text
if response.status_code == 200:
    print(" OCR-SPACE processing.")
    json_data = response.json()
    if json_data['IsErroredOnProcessing'] == False:
        extracted_text = json_data['ParsedResults'][0]['ParsedText']
        print(extracted_text)

    else:
        print("Pytesseract OCR processing.")
        text = tess.image_to_string(image_path)
        print(text)

# print(text)
else:
    print("Error occurred during request processing.")

########################################################################################################

# microsoft Azure API

# import requests
# import json

# subscription_key = 'YOUR_SUBSCRIPTION_KEY'
# endpoint = 'YOUR_ENDPOINT'

# ocr_url = endpoint + '/vision/v3.1/ocr'

# image_url = 'https://example.com/images/example.jpg'

# headers = {
#     'Ocp-Apim-Subscription-Key': subscription_key,
#     'Content-Type': 'application/json'
# }

# params = {
#     'language': 'en',
#     'detectOrientation': 'true'
# }

# data = {
#     'url': image_url
# }

# response = requests.post(ocr_url, headers=headers, params=params, json=data)
# response.raise_for_status()

# analysis = response.json()

# lines = [line['text'] for region in analysis['regions']
#          for line in region['lines']]
# text = '\n'.join(lines)

# print(text)
