# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Bozhang Zhou
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406


import socket
import ds_protocol

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  #TODO: return either True or False depending on results of required operation
  try:
    if message is None:
      message=""

    if message.strip() != "":
      publish_msg = True
    else:
      publish_msg = False
    
    if bio is not None and bio.strip()!= "":
      publish_bio = True
    else:
      publish_bio = False
    if not publish_msg and not publish_bio:
      return False
    with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect((server, port))

      send_stream = client.makefile("w")
      receive_stream = client.makefile("r")

      join = ds_protocol.join_msg(username, password)
      send_stream.write(join + '\r\n')
      send_stream.flush()

      response = receive_stream.readline()
      join_response = ds_protocol.extract_json(response)

      if join_response.type != "ok":
        return False  
      
      token=join_response.token

      if publish_msg == True:
        post = ds_protocol.post_msg(token, message)
        send_stream.write(post + '\r\n')
        send_stream.flush()

        response = receive_stream.readline()
        post_response = ds_protocol.extract_json(response)

        if post_response.type != "ok":
          return False
        
      if publish_bio:
        bio_message = ds_protocol.bio_msg(token, bio)
        send_stream.write(bio_message + '\r\n')
        send_stream.flush()

        response = receive_stream.readline()
        bio_response = ds_protocol.extract_json(response)

        if bio_response.type != "ok":
          return False
      return True
  except Exception:
    return False