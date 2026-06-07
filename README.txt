ICS 32 Assignment 4 - Direct Messenger

Name: Bozhang Zhou
Email: bozhangz@uci.edu
Student ID: 93213406

Project Description:
This program is a direct messaging client for the ICS 32 Distributed Social server.
The program uses a Tkinter GUI to allow users to log in, add contacts, send direct
messages, retrieve new messages, and view saved message history.

Files:
a4.py
- Runs the Tkinter GUI.
- Allows the user to log in, add contacts, send messages, and retrieve new messages.

ds_protocol.py
- Creates JSON messages for the DS server.
- Supports join, post, bio, direct message send, retrieve new messages, and retrieve all messages.
- Parses JSON responses from the server.

ds_messenger.py
- Contains the DirectMessage and DirectMessenger classes.
- Handles socket connection to the server.
- Sends direct messages.
- Retrieves new and all direct messages.

local_storage.py
- Saves contacts and message history locally.
- Creates local JSON files in the local_data folder.
- Allows old messages to be loaded again after the program is closed.

server.py
- Provided server file for testing the DS server.

How to Run:
1. Open a terminal and start the server:

python3 server.py

2. Open another terminal and run the GUI:

python3 a4.py

3. Login with a username and password.
4. Add another user as a contact.
5. Select the contact, type a message, and click Send.
6. The other user can login from another GUI window and click Retrieve New to receive messages.

Testing:
To check syntax, run:

python3 -m py_compile ds_protocol.py ds_messenger.py local_storage.py a4.py

If test files are included, run:

python3 -m pytest

Notes:
The program uses port 3001 for the DS server.
The GUI uses Tkinter.
Messages are saved locally in JSON format.
The local_data folder and store folder are generated while running the program and do not need to be submitted.