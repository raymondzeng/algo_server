import sys
from flask import Flask, render_template

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

app = Flask(__name__)

class AlgoClient(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)

    def dataReceived(self, data):
        print data

        # disconnect from server once request acknowledged
        if data == 'received\n':
            self.transport.loseConnection()

def connected_to_algo(prot):
    """ 
    This function is run when a connection to the CoMet server has 
    been established and @prot is our interface to the server.
    """
    prot.sendMessage("Hello")


@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_algo():
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 5555)
    deferred = connectProtocol(endpoint, AlgoClient())
    # TODO check for connection fail
    deferred.addCallback(connected_to_algo)
    return 'Submitted'

if __name__ == '__main__':
    # run Flask app under twisted
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(resource)
    reactor.listenTCP(8000, site)
    
    # start the twisted event loop
    reactor.run()

