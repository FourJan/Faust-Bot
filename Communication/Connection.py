import socket
import re

from Communication.PingObservable import PingObservable
from Communication.PrivmsgObservable import PrivmsgObservable
from Model import ConnectionDetails


class Connection(object):

    details = None
    irc = None
    instance = None

    @staticmethod
    def singleton():
        return Connection.instance;

    def send_channel(self, text):
        """
        Send to channel
        :return:
        """
        global details
        self.raw_send("PRIVMSG " + details.get_channel() + " :" + text[0:])
        print (text)

    def send_to_user(self, user, text):
        """
        Send to user
        :return:
        """
        self.raw_send('PRIVMSG ' + user + ' :' + text)

    def raw_send(self, message):
        self.irc.send(message.encode() + '\r\n'.encode())

    def receive(self):
        """
        receive from Network
        """
        data = self.irc.recv(4096)
        self.data = data
        data = data.decode('UTF-8', errors='replace')
        self.data = data
        data = data.rstrip()
        print(data)
        if data.find('PING') != -1:
            self._ping.input(data)
        if data.find('PRIVMSG') != -1:
            self._privmsg.input(data)

    def last_data(self):
        return self.data

    def establish(self):
        """
        establish the connection
        """
        global details
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.irc.connect((details.get_server(), details.get_port()))
        print(self.irc.recv(4096))
        self.irc.send("NICK ".encode() + details.get_nick().encode() + "\r\n".encode())
        self.irc.send("USER botty botty botty :IRC Bot\r\n".encode())
        self.irc.send("JOIN ".encode() + details.get_channel().encode() + '\r\n'.encode())

    def __init__(self, set_details: ConnectionDetails):
        global details
        details = set_details
        self._ping = PingObservable()
        self._privmsg = PrivmsgObservable()
        if Connection.instance != None:
            raise ReferenceError("Only one connection is supported, don't create a new one as long as one still exists!")
        Connection.instance = self

    def observePing(self, observer):
        """
        add observer to the observers of the ping-observable
        :param observer: observer to add
        """
        self._ping.addObserver(observer)

    def observePrivmsg(self, observer):
        """
        add observer to the observers of the ping-observable
        :param observer: observer to add
        """
        self._privmsg.addObserver(observer)
