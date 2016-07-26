from __future__ import print_function

import json
import os
import sys
from collections import namedtuple
from pprint import pprint
from flask import Flask, request, jsonify
from twilio.twiml import Response
from twilio.rest import TwilioRestClient

TwilioConfig = namedtuple(
    'TwilioConfig',
    ['account_sid', 'auth_token', 'sender']
)

APP = Flask(__name__)

CONFIG_FILE = 'twilio.json'

class APIError(Exception):
    """Exception type to be raised when API encounters an error."""

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        dict_ = dict(self.payload or ())
        dict_['message'] = self.message
        return dict_


def read_config():
    """Read config from the environment or a config file."""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    sender = os.getenv('TWILIO_SENDER')
    if all([account_sid, auth_token, sender]):
        return TwilioConfig(account_sid, auth_token, sender)

    with open(CONFIG_FILE, 'r') as conf_file:
        contents = json.load(conf_file)
        if all(
                [
                    key in contents
                    for key in ['account_sid', 'auth_token', 'sender']
                ]
        ):
            return TwilioConfig(
                contents['account_sid'],
                contents['auth_token'],
                contents['sender']
            )

    raise ValueError(
        """Bad configuration:
        set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SENDER
        in environment, or
        create twilio.json file with "account_sid", "auth_token", "sender"
        as object keys.
        """
    )


@APP.route("/", methods=['GET', 'POST'])
def respond():
    """Respond to incoming messages with a simple response."""
    resp = Response()
    resp.message('I don\'t care what you say. http://www.pizzaparty.me')
    return str(resp)


@APP.route("/send/<int:recipient_number>", methods=['POST'])
def send(recipient_number):
    """Send a message to the phone number provided in the path."""
    client = TwilioRestClient(CONF.account_sid, CONF.auth_token)
    body = request.get_json()
    if not body or not body.get('message'):
        raise APIError('Send JSON with "message" property for message body.', 400)

    message = client.messages.create(
        to=recipient_number,
        from_=CONF.sender,
        body=body.get('message')
    )
    return jsonify({
        'message_sid': message.sid
    })


@APP.errorhandler(APIError)
def handle_bad_request(err):
    """Handle bad requests."""
    response = jsonify(err.to_dict())
    response.status_code = err.status_code
    return response


try:
    CONF = read_config()
except ValueError as ex:
    print(str(ex))
    sys.exit(1)

pprint(CONF)


if __name__ == "__main__":
    APP.run(debug=True)
