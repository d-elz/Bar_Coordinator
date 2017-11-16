from twisted.internet.task import deferLater
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor, endpoints , ssl
from twisted.web.server import Site

import sys , os

#Our imports
from bar0.coordinator.security_staff import signature
from bar0.coordinator.operations import DatabaseOperationCoordinator
import cgi
from bar0.coordinator.common.funcs import dirc

sslContext = ssl.DefaultOpenSSLContextFactory(
    dirc(__file__,'../keys/server_keys',"/server.key"),  # Private Key
    dirc(__file__,'../keys/server_keys',"/server.crt"),  # Certificate
)


class DelayedResource(Resource):
    def _delayedRender(self, request):
        RESPONSE = "<html><body>You submitted:" + cgi.escape(request.args["nym"][0]) + cgi.escape(request.args["pk"][0]) +"</body></html>"
        request.write(RESPONSE)
        request.finish()

    def render_GET(self, request):
        return '<html><body><form method="POST">Nym:<input name="nym" type="text" />PK:<input name="pk" type="text" /><input type="submit" value="Submit"></form></body></html>'

    def render_POST(self, request):
        d = deferLater(reactor, 1, lambda: request)
        d.addCallback(self.register_service)
        return NOT_DONE_YET

    def register_service(self , request):

        nym = cgi.escape(request.args["nym"][0])
        pk = cgi.escape(request.args["pk"][0])
        print nym +pk
        ##### Cheking the Nym if exist in database
        database_coor = DatabaseOperationCoordinator()
        checking = database_coor.checking_pseudonym(nym)

        #Getting the axact path of private key
        dir_of_executable = os.path.dirname(__file__)
        path_to_private_key = os.path.abspath(os.path.join(dir_of_executable, '../keys')) + "/private_key"

        print path_to_private_key
        data_to_sign = nym +"|"+ pk
        sign= signature.sign(data_to_sign , path_to_private_key)

        #Getting the exact path of public key
        path_to_public_key = os.path.abspath(os.path.join(dir_of_executable, '../keys')) + "/public_key"
        ver= signature.verify(data_to_sign , path_to_public_key,sign)
	print "something"
        if not checking:
            database_coor.insert_public_list(nym, pk ,sign )
            RESPONSE = "<html><body>You submitted:" + cgi.escape(request.args["nym"][0]) + cgi.escape(request.args["pk"][0]) + "</body></html>"
            request.write(RESPONSE)
            request.finish()
        else:
            RESPONSE = "<html><body>There is a user with the same name! </body></html>"
            request.write(RESPONSE)
            request.finish()

def web_register_service():
    root = Resource()
    root.putChild("register", DelayedResource())
    factory = Site(root)
    #endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
    #endpoint.listen(factory)

    #With SSL
    reactor.listenSSL(443, factory, sslContext)
    reactor.run()

if __name__ == "__main__":
    web_register_service()
