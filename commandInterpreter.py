import json
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory as ClF
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

class Client(Protocol):
	def dataReceived(self, data):
		data = data.decode('utf-8')
		print(data)
		command = (input().split())
		data = json.dumps({"command": command[0], "id": command[1]})
		self.transport.write(data.encode())

class ClientFactory(ClF):
	def buildProtocol(self, addr):
		return Client()

point = TCP4ClientEndpoint(reactor, "localhost", 5678)
point.connect(ClientFactory())
reactor.run()

# d = connectProtocol(point, Server())
# d.addCallback(gotProtocol)
#
# command = ["default"]
# operator = "default"
#

# print(data)
#
# reactor.run()
