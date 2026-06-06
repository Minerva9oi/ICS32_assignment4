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

            self.friends = data.get("friends", [])
            self.messages = data.get("messages", {})

        except Exception:
            self.friends = []
            self.messages = {}

    def save(self):
        data = {
            "username": self.username,
            "friends": self.friends,
            "messages": self.messages
        }

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
            timestamp = str(time.time())

        new_message = {
            "sender": sender,
            "message": message,
            "timestamp": timestamp
        }

        self.messages[contact].append(new_message)
        self.save()

    def get_messages(self, contact):
        if contact in self.messages:
            return self.messages[contact]

        return []

    def add_sent_message(self, recipient, message, timestamp=None):
        self.add_message(recipient, self.username, message, timestamp)


    def add_received_message(self, sender, message, timestamp=None):
        self.add_message(sender, sender, message, timestamp)