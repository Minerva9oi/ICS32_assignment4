# NAME Bozhang Zhou 
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406


import json
import time
from pathlib import Path


class LocalStorage:
    def __init__(self, username, folder="local_data"):
        self.username = username

        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)

        self.path = self.folder / f"{username}_messages.json"

        self.friends = []
        self.messages = {}

        self.load()

    def load(self):
        if not self.path.exists():
            self.save()
            return

        try:
            file = open(self.path, "r")
            data = json.load(file)
            file.close()

            if "friends" in data:
                self.friends = data["friends"]
            else:
                self.friends = []

            if "messages" in data:
                self.messages = data["messages"]
            else:
                self.messages = {}

        except Exception:
            self.friends = []
            self.messages = {}

    def save(self):
        data = {}
        data["username"] = self.username
        data["friends"] = self.friends
        data["messages"] = self.messages

        file = open(self.path, "w")
        json.dump(data, file, indent=4)
        file.close()

    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)

        if friend not in self.messages:
            self.messages[friend] = []

        self.save()

    def get_friends(self):
        return self.friends

    def add_message(self, contact, sender, message, timestamp=None):
        self.add_friend(contact)

        if timestamp is None:
            new_timestamp = str(time.time())
        else:
            new_timestamp = timestamp

        new_message = {}
        new_message["sender"] = sender
        new_message["message"] = message
        new_message["timestamp"] = new_timestamp

        self.messages[contact].append(new_message)

        self.save()

    def get_messages(self, contact):
        if contact in self.messages:
            contact_messages = self.messages[contact]
            return contact_messages
        else:
            return []

    def add_direct_message(self, direct_message):
        contact = direct_message.recipient
        sender = direct_message.recipient
        message = direct_message.message
        timestamp = direct_message.timestamp

        self.add_message(contact, sender, message, timestamp)