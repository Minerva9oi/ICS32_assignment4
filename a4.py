# NAME Bozhang Zhou 
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406


import tkinter as tk

from ds_messenger import DirectMessenger
from local_storage import LocalStorage


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ICS32 Direct Messenger")

        self.messenger = None
        self.storage = None
        self.current_contact = None

        self._build_login_area()
        self._build_main_area()
        self._build_status_area()

    def _build_login_area(self):
        login_frame = tk.Frame(self.root)
        login_frame.pack(fill=tk.X, padx=10, pady=10)

        server_label = tk.Label(login_frame, text="Server:")
        server_label.grid(row=0, column=0)

        self.server_entry = tk.Entry(login_frame, width=15)
        self.server_entry.insert(0, "127.0.0.1")
        self.server_entry.grid(row=0, column=1)

        username_label = tk.Label(login_frame, text="Username:")
        username_label.grid(row=0, column=2)

        self.username_entry = tk.Entry(login_frame, width=15)
        self.username_entry.grid(row=0, column=3)

        password_label = tk.Label(login_frame, text="Password:")
        password_label.grid(row=0, column=4)

        self.password_entry = tk.Entry(login_frame, width=15, show="*")
        self.password_entry.grid(row=0, column=5)

        self.login_button = tk.Button(login_frame, text="Login",
                                      command=self.login)
        self.login_button.grid(row=0, column=6, padx=5)

    def _build_main_area(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        contact_label = tk.Label(left_frame, text="Contacts")
        contact_label.pack()

        self.friend_listbox = tk.Listbox(left_frame, width=20)
        self.friend_listbox.pack(fill=tk.Y, expand=True)
        self.friend_listbox.bind("<<ListboxSelect>>", self.select_friend)

        add_label = tk.Label(left_frame, text="Add User:")
        add_label.pack(pady=(8, 0))

        self.add_friend_entry = tk.Entry(left_frame, width=20)
        self.add_friend_entry.pack(fill=tk.X)

        self.add_button = tk.Button(left_frame, text="Add",
                                    command=self.add_user)
        self.add_button.pack(fill=tk.X, pady=5)

        self.retrieve_button = tk.Button(left_frame, text="Retrieve New",
                                         command=self.retrieve_new_messages)
        self.retrieve_button.pack(fill=tk.X)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.chat_display = tk.Text(right_frame, height=20,
                                    state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(right_frame)
        bottom_frame.pack(fill=tk.X, pady=5)

        self.message_entry = tk.Entry(bottom_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(bottom_frame, text="Send",
                                     command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)

    def _build_status_area(self):
        self.status_label = tk.Label(self.root, text="Please login first.")
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 10))

    def set_status(self, text):
        self.status_label.config(text=text)

    def login(self):
        server = self.server_entry.get()
        server = server.strip()

        username = self.username_entry.get()
        username = username.strip()

        password = self.password_entry.get()
        password = password.strip()

        if server == "":
            self.set_status("Error: server is required.")
            return

        if username == "":
            self.set_status("Error: username is required.")
            return

        if password == "":
            self.set_status("Error: password is required.")
            return

        new_messenger = DirectMessenger(server, username, password)

        login_result = new_messenger.login()

        if login_result == False:
            self.set_status("Error: login failed.")
            return

        self.messenger = new_messenger
        self.storage = LocalStorage(username)

        self.load_friends()

        self.set_status("Login successful.")

        self.root.after(5000, self.auto_retrieve_new)

    def load_friends(self):
        self.friend_listbox.delete(0, tk.END)

        if self.storage is None:
            return

        friends = self.storage.get_friends()

        for friend in friends:
            self.friend_listbox.insert(tk.END, friend)

    def add_user(self):
        if self.storage is None:
            self.set_status("Error: please login first.")
            return

        friend = self.add_friend_entry.get()
        friend = friend.strip()

        if friend == "":
            self.set_status("Error: enter a username to add.")
            return

        self.storage.add_friend(friend)

        self.add_friend_entry.delete(0, tk.END)

        self.load_friends()

        self.set_status("Added user: " + friend)

    def select_friend(self, event):
        selection = self.friend_listbox.curselection()

        if len(selection) == 0:
            return

        index = selection[0]

        selected_friend = self.friend_listbox.get(index)
        self.current_contact = selected_friend

        self.show_messages()

        self.set_status("Selected contact: " + self.current_contact)

    def show_messages(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)

        if self.storage is None:
            self.chat_display.config(state=tk.DISABLED)
            return

        if self.current_contact is None:
            self.chat_display.config(state=tk.DISABLED)
            return

        messages = self.storage.get_messages(self.current_contact)

        for msg in messages:
            if "sender" in msg:
                sender = msg["sender"]
            else:
                sender = ""

            if "message" in msg:
                message = msg["message"]
            else:
                message = ""

            line = sender + ": " + message + "\n"

            self.chat_display.insert(tk.END, line)

        self.chat_display.config(state=tk.DISABLED)

    def send_message(self):
        if self.messenger is None:
            self.set_status("Error: please login first.")
            return

        if self.storage is None:
            self.set_status("Error: please login first.")
            return

        if self.current_contact is None:
            self.set_status("Error: please select a contact first.")
            return

        message = self.message_entry.get()
        message = message.strip()

        if message == "":
            self.set_status("Error: message cannot be empty.")
            return

        send_result = self.messenger.send(message, self.current_contact)

        if send_result == True:
            self.storage.add_message(self.current_contact, "me", message)

            self.message_entry.delete(0, tk.END)

            self.show_messages()

            self.set_status("Message sent.")
        else:
            self.set_status("Error: message was not sent.")

    def retrieve_new_messages(self):
        if self.messenger is None:
            self.set_status("Error: please login first.")
            return

        if self.storage is None:
            self.set_status("Error: please login first.")
            return

        new_messages = self.messenger.retrieve_new()

        count = 0

        for msg in new_messages:
            self.storage.add_direct_message(msg)
            count = count + 1

        self.load_friends()

        self.show_messages()

        self.set_status("Retrieved " + str(count) + " new message(s).")

    def auto_retrieve_new(self):
        if self.messenger is not None and self.storage is not None:
            new_messages = self.messenger.retrieve_new()

            count = 0

            for msg in new_messages:
                self.storage.add_direct_message(msg)
                count = count + 1

            if count > 0:
                self.load_friends()
                self.show_messages()
                self.set_status("Auto retrieved " + str(count) +
                                " new message(s).")

        self.root.after(5000, self.auto_retrieve_new)


def main():
    root = tk.Tk()
    ChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()