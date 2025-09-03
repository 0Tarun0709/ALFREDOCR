
# import requests
# from PIL import Image
# import pytesseract as tess
# import http
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# api_key = 'K86847055688957'
# image_path = '.\images\img2.png'

# # Send a POST request to OCR.Space API with the image file and API key
# response = requests.post('https://api.ocr.space/parse/image',
#                          files={'image': open(image_path, 'rb')},
#                          data={'apikey': api_key})

# # Parse the JSON response and extract the text
# if response.status_code == 200:
#     print(" OCR-SPACE processing.")
#     json_data = response.json()
#     if json_data['IsErroredOnProcessing'] == False:
#         extracted_text = json_data['ParsedResults'][0]['ParsedText']
#         print(extracted_text)

#     else:
#         print("Pytesseract OCR processing.")
#         text = tess.image_to_string(image_path)
#         print(text)

# # print(text)
# else:
#     print("Error occurred during request processing.")



import easyocr
reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
result = reader.readtext(r"C:\Users\z0052mvs\Pictures\Screenshots\Screenshot 2025-08-18 183252.png")

print(result)