from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utility import fetch_reply

app = Flask(__name__)

@app.route("/")
def index():
	return "Hello, World!"


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	fulfillmentText = ''
	sum = 0
	query_result = req.get('queryResult')
	if query_result.get('action') == 'orderinfo':
		num1 = int(query_result.get('parameters').get('number'))
		print('here num1 = {0}'.format(num1))
		fulfillmentText = 'The order numbers is {0} and \n and It is under processing !!!'.format(num1)
		return {
		"fulfillmentText": fulfillmentText,
		"displayText": '25',
		"source": "webhookdata"
	}

	# Fetch the message
	msg = request.form.get('Body')
	phone_no = request.form.get('From')
	reply = fetch_reply(msg, phone_no)
	"""
	if(msg.lower() == "hello"):
		reply = "Hi! \n How can i help you?" 
	else:
		reply = "Hi! \nI am MLL Virtual Assistance.\nI am in developing mode.\nThanks."
	"""
	response = MessagingResponse()
	response.message(reply)


@app.route("/sms", methods=['POST'])
def reply():

	# Fetch the message
	msg = request.form.get('Body')
	phone_no = request.form.get('From')
	reply = fetch_reply(msg, phone_no)
	"""
	if(msg.lower() == "hello"):
		reply = "Hi! \n How can i help you?" 
	else:
		reply = "Hi! \nI am MLL Virtual Assistance.\nI am in developing mode.\nThanks."
	"""
	response = MessagingResponse()
	response.message(reply)

	return str(response)

if __name__ == "__main__":
	app.run(debug=True)