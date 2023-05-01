import openai
import pyttsx3
import requests
from PIL import Image
import pytesseract as tess
import requests

# API Section
openai.api_key = "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"
api_key = 'K86847055688957'
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


image_path = './images/img3.png'

engine=pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

messages = []


system_msg = input("What type of chatbot would you like to create?\n")
engine.say("What type of chatbot would you like to create?")
engine.runAndWait()

messages.append({"role": "system", "content": system_msg})

print("Your Alferd.ai is ready!")

engine.say("Im ALFERD.ai Im ready to answer your Questions!")
engine.runAndWait()
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")
    
    engine.say(reply)
    engine.runAndWait()
    
    ## image to text code
    print(" OCR-SPACE processing.")
    
    response = requests.post('https://api.ocr.space/parse/image',
                             files={'image': open(image_path, 'rb')},
                             data={'apikey': api_key})
    if response.status_code == 200:
        json_data = response.json()
        if json_data['IsErroredOnProcessing'] == False:
            extracted_text = json_data['ParsedResults'][0]['ParsedText']
            print(extracted_text)
        else:
            print("Pytesseract OCR processing.")
            extracted_text = tess.image_to_string(image_path)
            print(extracted_text)
    else:
        print("Error occurred during request processing.")
        
    message = extracted_text
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")
    
    
    
    