from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utility import fetch_reply
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
	return "Hello, World!"



def kpiinsertion(contactno,userid,kpicount,kpidate):
	API_ENDPOINT = "https://quiet-brook-50483.herokuapp.com/api/v1/adduserkpidetail/"
	data = {
    	"userid": userid,
    	"contactno": contactno,
    	"kpicount": kpicount,
    	"kpidate": kpidate
	}
	r = requests.post(url = API_ENDPOINT, data = data)
	return r.text


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	phone_no = request.form.get('From')
	fulfillmentText = ''
	sum = 0
	sessiondetail = req['session'].split('/')[-1]
	whatsupno = sessiondetail.split('+')[-1][2:]
	# print("whatsupno {0}".format(whatsupno))
	query_result = req.get('queryResult')
	if query_result.get('action') == 'orderinfo':
		num1 = int(query_result.get('parameters').get('number'))
		fulfillmentText = 'The order numbers is {0} and \n and It is under processing !!!'.format(num1)
		return {
		"fulfillmentText": fulfillmentText,
		"displayText": '25',
		"source": "webhookdata"
		}
	if query_result.get('action') == 'addkpi':
		kpicount = int(query_result.get('parameters').get('number'))
		datestr = str(query_result.get('parameters').get('date'))
		print('here num1 = {0}'.format(datestr[:10]))
		kpidate = datetime.strptime(datestr[:10],'%Y-%m-%d').date()
		# print('here it is {0}'.format(whatsupno))
		userid = '1111'
		message = kpiinsertion(whatsupno,userid,kpicount,kpidate)
		fulfillmentText = 'Your kpi {0} on \n {1} is captured!!!'.format(kpicount,kpidate)
		return {
		"fulfillmentText": fulfillmentText,
		"displayText": '25',
		"source": "webhookdata"
		}
	msg = request.form.get('Body')
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