# Twilio: Getting Started with Programmatic SMS #

This is a Python Flask server that sends and receives SMS text messages. It is
based on Twilio's own example for getting started with Python, but provides a
little more configurability.

## Setup ##

I suggest you use a Python virtualenv to keep things clean, and run
```pip install -r requirements.txt```

You'll also need to set up configuration. You can export environment variables:

```
export TWILIO_ACCOUNT_SID=<your account SID>
export TWILIO_AUTH_TOKEN=<your auth token>
export TWILIO_SENDER=<your Twilio number that will send SMS>
```
or you can create a `twilio.json` file in the same directory as the app:
```json
{
    "account_sid": "<your account SID>",
    "auth_token": "<your auth token>",
    "sender": "<your Twilio number that will send SMS>"
}
```

A sample `twilio.json` has been provided for your convenience.

## Running ##
```
$ export FLASK_APP=sms.py
$ flask run
```
or
```
$ python sms.py
```

## Using ##

There are two endpoints: one for sending messages, and one for responding to
received messages.

### Sending ###

The endpoint is `/send`, and it takes a path parameter that indicates the
recipient number, like `/send/2025550143`. (That's a [fake
number](https://fakenumber.org), if you were wondering).

The request body contains a JSON document with an object with a `message`
property, which will be the message that is sent to the recipient. Don't forget
to send a `Content-Type: application/json` header.

#### Curl example ####
```
curl -d'{"message": "This is the message that will be sent."}' -H'Content-Type: application/json' localhost:5000/send/2025550143
```

### Receiving ###

The receiving endpoint is the root of the webapp, `/`.

The receiving endpoint isn't hit directly by a user, but rather called by
Twilio to respond to incoming messages. 

#### Setup ####

You'll have to expose the app to the internet so Twilio can reach it. This is
really easy with [ngrok](https://ngrok.com/), or you can [deploy to
Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
if you want something more long-lived than ngrok can offer. For
experimentation, though, ngrok works nicely.

You'll also need to configure the number you're using to send messages to use
the URL corresponding to where your app is running, which can be done from the
[Twilio Console](https://www.twilio.com/console/phone-numbers/incoming), by
clicking on the number you wish to configure and setting its Messaging Webhook.

## Notes ##

This was developed with Python 3.5.2, and has not been tested with any other
versions.
