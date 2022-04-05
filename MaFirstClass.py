import argparse
import socket

class Hacker:

    def __init__(self, ipaddress: str, port: str) -> None:
        """
        Hacker class initiator
        :param ipaddress: str IP Address in string format
        :param port: str port number in string format
        :return: None
        """
        self._ipaddress = ipaddress
        self._port = port
        self.buffer_size = 1024

    def socket_run(self, message: str) -> str:
        """
        Method to create a socket, connect and return response
        :param message: str password in string format
        :return: str server response in string format
        """

        #  Creating a tuple of ip address and port
        ipaddress = (self._ipaddress, int(self._port))
        #  Create a socket object and connect using provided parameters
        with socket.socket() as client_socket:
            client_socket.connect(ipaddress)
            #  Convert string message to bytes
            message = message.encode()
            #  Send an encoded message to server
            client_socket.send(message)
            #  Receive response in string format
            response = client_socket.recv(self.buffer_size).decode()
        return response

if __name__ == '__main__':
    #  Instantiate ArgumentParser class
    parser = argparse.ArgumentParser()
    parser.add_argument('ipaddress')
    parser.add_argument('port')
    parser.add_argument('message')
    #  Read arguments from command line
    args = parser.parse_args()
    host = str(args.ipaddress)
    port = int(args.port)
    message = str(args.message)
    # Instantiate Hacker class
    hacker = Hacker(host, port)
    #  Get response from server
    response = hacker.socket_run(message)
    #  print response
    print(response)
