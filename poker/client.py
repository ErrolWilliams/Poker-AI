
class Client(object):
    def __init__(self, server, playername):
        self.server = server
        self.playername = playername

    def connect(self):
        print(f"Connecting to '{self.server}' as '{self.playername}' ...")

    def run(self):
        self.connect()


def some_fun():
    print("Hello there!")
