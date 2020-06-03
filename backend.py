import json
import apiai
from flask import Flask
import twilio.twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client

# Twilio account info
account_sid = ""
auth_token = ""
account_num = ""
client = Client(account_sid, auth_token)

# Google Dialogflow account info
CLIENT_ACCESS_TOKEN = ""
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello api.ai (from Flask!)'

@app.route("/", methods=['GET', 'POST'])
def server():
    from flask import request
    # get SMS input via twilio
    resp = twilio.twiml.messaging_response.MessagingResponse()

    # get SMS metadata
    msg_from = request.values.get("From", None)
    msg = request.values.get("Body", None)

    # prepare Dialogflow request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = msg

    # get response from Google Dialoglow API
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
        # send SMS response back via twilio
        #client.messages.create(to=msg_from, from_= account_num, body=response)
        resp.message(response)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
