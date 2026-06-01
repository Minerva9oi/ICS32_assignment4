# NAME Bozhang Zhou 
# EMAIL bozhangz@uci.edu
# STUDENT ID 93213406


import socket
import ds_protocol

PORT = 3001


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None


    def _send_command(self, writer, command):
        writer.write(command + "\r\n")
        writer.flush()

    
    def _connect_and_join(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.dsuserver, PORT))

            reader = client_socket.makefile("r")
            writer = client_socket.makefile("w")

            join_command = ds_protocol.join_msg(self.username, self.password)
            self._send_command(writer, join_command)

            response = reader.readline()
            join_response = ds_protocol.extract_json(response)

            if join_response.type == "ok":
                self.token = join_response.token
                return client_socket, reader, writer

            client_socket.close()
            return None, None, None

        except Exception:
            return None, None, None
    
    def send(self, message, recipient):
        client_socket, reader, writer = self._connect_and_join()

        if client_socket is None:
            return False

        try:
            dm_command = ds_protocol.direct_message_msg(
                self.token,
                message,
                recipient
            )

            self._send_command(writer, dm_command)

            response = reader.readline()
            dm_response = ds_protocol.extract_json(response)

            return dm_response.type == "ok"

        except Exception:
            return False

        finally:
            client_socket.close()


    def retrieve_new(self):
        return self._retrieve_messages("new")

    def retrieve_all(self):
        return self._retrieve_messages("all")
    

    def _retrieve_messages(self, message_type):
        client_socket, reader, writer = self._connect_and_join()

        if client_socket is None:
            return []

        try:
            if message_type == "new":
                command = ds_protocol.direct_message_new_msg(self.token)
            else:
                command = ds_protocol.direct_message_all_msg(self.token)

            self._send_command(writer, command)

            response = reader.readline()
            result = ds_protocol.extract_json(response)

            if result.type != "ok":
                return []

            messages = []

            for item in result.messages:
                dm = DirectMessage()

                if "from" in item:
                    dm.recipient = item["from"]
                elif "recipient" in item:
                    dm.recipient = item["recipient"]

                dm.message = item.get("message")
                dm.timestamp = item.get("timestamp")

                messages.append(dm)

            return messages

        except Exception:
            return []

        finally:
            client_socket.close()