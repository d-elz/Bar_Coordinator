from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol , ssl , threads

from twisted.internet.defer import Deferred

from twisted.web.server import NOT_DONE_YET
from twisted.internet.task import deferLater

from twisted.internet.endpoints import TCP4ServerEndpoint , SSL4ServerEndpoint

import sys , os , time
from datetime import date
import urllib2

#Our imports
from bar0.coordinator.operations import  RegisterCoordinator , LogInOutCoordinator , DatabaseOperationCoordinator  ,ExchangeKeyCoordinator , Coordinator , BarServerCoordinator
from bar0.coordinator.common.funcs import dirc

sslContext = ssl.DefaultOpenSSLContextFactory(
    dirc(__file__,'../keys/server_keys',"/server.key"),  # Private Key
    dirc(__file__,'../keys/server_keys',"/server.crt"),  # Certificate
)

BAR_SERVER = urllib2.urlopen('http://ip.42.pl/raw').read()
BAR_SERVER_PORT1 = 6888
BAR_SERVER_PORT2 = 6889

####  USER REGISTRATION PROTOCOL  ####

bar_servers = []

class UserRegistrationProtocol(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory #

    ## The connectionMade event is usually where setup of the connection object happens
    def connectionMade(self):
        peer = self.transport.getPeer()
        host = self.transport.getHost()

        print "~~ Connection established from " + str(peer)

        self.factory.numConnections += 1
        self.factory.logs(peer)
        print "Number of active connections: %d" % (self.factory.numConnections,)

    #Called when data is received across a transport.
    def dataReceived(self, data):
        #REGISTER Service
        if data.split('||||')[0] == "Register":
            print "~~ Client use the Register Service"
            rg = RegisterCoordinator()
            db = DatabaseOperationCoordinator()

            #Checking pseudonym and send feedback to the client
            nym = data.split('||||')[1]
            check_nym_exist = db.checking_pseudonym(nym)

            if check_nym_exist:
                reactor.callInThread(rg.coordinator_operation, data) # Using threads to call the function coordinator_operation
                self.transport.write("Register||||0") # sending the message to client
            else:
                self.transport.write("Register||||-1")
        #LOG IN Service
        elif data.split('||||')[0] == "LogIn":
            print "~~ Client use the LogIn Service"
            lin = LogInOutCoordinator()
            db = DatabaseOperationCoordinator()
            #cij = db.select_exchange_list(data.split('||||')[1])
            #kos = threads.deferToThread(lin.coordinator_operation , data )
            user_logged_in , bar_server = lin.login( data)
            if user_logged_in:
                #if cij:
                    #ex = "LogIn||||0||||"+str(cij)
                    #self.transport.write(ex)
                #else:
                self.transport.write("LogIn||||"+str(bar_server))#if the user logged in successfully send the BAR server IP and port.
            else:
                self.transport.write("LogIn||||-1")#if the user doesn t logged in successfully send error byte -1
        #LOG OUT Service
        elif data.split('||||')[0] == "LogOut":
            print "~~ CLient use the LogOut Service"
            peer = self.transport.getPeer()
            lout = LogInOutCoordinator()
            #d = threads.deferToThread(li.coordinator_operation , data , peer)
            reactor.callInThread(lout.logout, data)
            self.transport.write("LogOut||||1")
            print "User successfully logged out"
        elif data.split('||||')[0] == "ExchangeKey":
            print "~~ CLient use the ExchangeKey Service"
            peer = self.transport.getPeer()
            ekc = ExchangeKeyCoordinator()
            #d = threads.deferToThread(li.coordinator_operation , data , peer)
            reactor.callInThread(ekc.coordinator_operation, data)
            self.transport.write("ExchangeKey||||User has successfully exchange keys!")
        elif data.split('||||')[0] == "BarServer":
            print "~~ Bar Server use the BarServer Service"
            bar_servers.append(self) # Keep track of the bar Servers
            bs = BarServerCoordinator()
            reactor.callInThread(bs.coordinator_operation, data)
            self.bar_server_unique_name = data.split('||||')[3]
            self.transport.write("BarServer||||The Bar server registers!")
        else:
            print "~~ CLient using nothing.He can t procced"
            print "Garbage : " + data


    ## The connectionLost event is where tearing down of any connection-specific objects is done
    def connectionLost(self, reason):
        #Messages to connectionLost
        peer = self.transport.getPeer()
        print "~~ Disconnecting from  " + str(peer)
        if self in bar_servers: # If the disconnected user is a Bar Server
            bs = BarServerCoordinator()
            bs.bar_server_logout(self.bar_server_unique_name)
            bar_servers.remove(self)
        self.factory.numConnections -= 1


class UserRegistrationFactory(Factory):

    numConnections = 0
    data = ""
    method = ""#Register or LogIn

    def __init__(self , FileName):
        self.file = FileName

    def buildProtocol(self, addr):
        return UserRegistrationProtocol(self)

    def startFactory(self):
        self.fp = open(self.file, 'a')
        print "The server started..."

    def stopFactory(self):
        self.fp.close()

    def logs(self,peer):
        self.fp = open(self.file, 'a')
        log = "Bar[" + time.asctime(time.localtime()) + "] from "+ str(peer) + " with method: " + "\r"
        self.fp.write(log)

def register_service():

    #Simple TCP communication stream on port 8000(waiting(listening) connection)
	#reactor.listenTCP(8000, UserRegistrationFactory())

	#SSL
    reactor.listenSSL(443, UserRegistrationFactory("logs.log") ,sslContext)

    #SSL with endPoints
    #endpoint = SSL4ServerEndpoint(reactor, 443 ,sslContext )
    #endpoint.listen(UserRegistrationFactory("logs.log")) #endpoint.listen() tells the reactor to handle connections to the endpoints address using a particular protocol
    reactor.run()

if __name__ == '__main__':
	register_service()
