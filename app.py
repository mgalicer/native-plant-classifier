from flask import Flask, request
from twilio.twiml.messaging_response import Body, Message, MessagingResponse
from fastai.vision import *
import requests
import torch

defaults.device = torch.device('cpu')
learn = load_learner('data')

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def sms_reply():
    print("got a request")
    # initalize messaging response object 
    resp = MessagingResponse()

    # handle case if someone sends a text 
    textBody = request.values.get('Body', None)
   
    if textBody != None and len(textBody) > 0:
        resp.message("Sorry, I don't understand texts! Please send me a photo that I can classify for you :)")
        return str(resp)

    # get URL of media that Twilio sends
    photoURL = request.values.get('MediaUrl0', None)
    if photoURL == None:
        return

    # download url contents in binary format
    r = requests.get(photoURL)
    with open('photo.png', 'wb') as f:
        f.write(r.content)
    
    img = open_image('photo.png')

    #run the classification for the downloaded image and create a response string
    outputs = learn.predict(img)
    classification = str(outputs[0])
    accuracy = str('{:.1f}'.format(max(outputs[2]).item() * 100))
    resStr = "I'm " + accuracy + "% sure that\'s a " + classification   

    # return a message to the user telling them what kind of plant is in the photo!
    resp.message(resStr)
    return str(resp)

@app.route("/", methods=['GET'])
def home():
    print("got a get request")
    return "Hello, World!"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
