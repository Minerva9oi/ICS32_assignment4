# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Bozhang Zhou 
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406

import time
import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['type','message','token'])

def join_msg(username, password):
  msg = {
          "join":{
            "username":username,
            "password": password, 
            "token":""
            }
        }
  return json.dumps(msg)


def post_msg(token, message):
  msg = {
          "token":token, 
          "post": {
                "entry":message, 
                "timestamp":str(time.time())
                  }
          }
  return json.dumps(msg)


def bio_msg(token, bio):
  msg = {
        "token": token,
        "bio": {
          "entry": bio,
          "timestamp": str(time.time())
        }
  }
  return json.dumps(msg)


def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    response = json_obj["response"]

    response_type = response["type"]
    message = response["message"]

    if "token" in response:
      token = response ["token"]
    else:
      token = ""
    return DataTuple(response_type, message, token)
  
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
    return DataTuple("error", "Json cannot be decoded.", "")
  
  except KeyError:
    print("Invalid DSP response format")
    return DataTuple("error", "Invalid DSP response format", "")