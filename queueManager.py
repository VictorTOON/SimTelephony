import json
import enumerates
import myClasses
from queueLogic import *

command = ["default"]
operator = "default"
calls = []
ongoingCalls = []

#creating operators, could be a list
operatorA = myClasses.Operator("A")
operatorB = myClasses.Operator("B")

operators = [operatorA, operatorB]

def manage(server, data, operator, calls, ongoingCalls):
	command = [data["command"], data["id"]]
	operator, calls, ongoingCalls = queueLogic(command, operator, calls, ongoingCalls, operators, server)

class Server(Protocol):
	def connectionMade(self):
		print("Connected to the client")
		self.transport.write(json.dumps([json.dumps({"response": "Connected to the server"})]).encode('utf-8'))

	def dataReceived(self, data):
		manage(self, json.loads(data.decode()), operator, calls, ongoingCalls)

# def gotProtocol(p):
#     p.sendMessage("Hello")
#     reactor.callLater(1, p.sendMessage, "This is sent in a second")
#     reactor.callLater(2, p.transport.loseConnection)

class ServerFactory(ServF):
	def buildProtocol(self, addr):
		return Server()

point = TCP4ServerEndpoint(reactor, 5678)
point.listen(ServerFactory())
reactor.run()

# reactor.listenTCP(5678, ChatFactory())
# reactor.run()

# d = connectProtocol(point, Server())
# d.addCallback(gotProtocol)
