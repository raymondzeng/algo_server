import sys
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class Algo(Protocol):
    def connectionMade(self):
        self.transport.write("connected\n")

    def connectionLost(self, reason):
        print "connection lost:", reason

    def dataReceived(self, data):
        print data
        self.transport.write("received\n")

class AlgoFactory(Factory):
    def buildProtocol(self, addr):
        return Algo()

if __name__ == "__main__":
    port = int(sys.argv[1]) # port num. is first and only parameter 
    reactor.listenTCP(port, AlgoFactory())
    reactor.run()
