from background_task import background
import firebase_admin
from firebase_admin import credentials, firestore,db
from firebase_admin import messaging
import os, sys
import json
import ast
######
from django.core.management import call_command
call_command('process_tasks')
######
@background(schedule=1)
def send_message():
    # The topic name can be optionally prefixed with "/topics/".
    topic = 'track_location'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'message': "Tracking your Location",
        },
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_topic]

send_message(repeat=20,repeat_until=None)
