import json
from myClasses import *
from enumerates import *
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServF
from twisted.internet.endpoints import TCP4ServerEndpoint, connectProtocol

def availableOperator(operators):
	#print(operators[0].getState(), operators[1].getState())
	for operator in operators:
		if operator.getState() == switchState(0):
			return operator
	return 0

def queueLogic(command, operator, calls, ongoingCalls, operators, server):
	print(command[0])
	my_json = []
	missed = 0
	#list of commands to be called
	#for every command and ID in the list, checks everything
	match command[0]:
		case "call":
			#server.transport.write(json.dumps({"response": ("call " + str(command[1]) +" received\n")}).encode())
			my_json.append(json.dumps({"response": ("call " + str(command[1]) +" received")}))
			#creates a call with an id
			calls.append(Call(command[1]))

		case "answer":
			#find operator
			for operator in operators:
				if operator.getId() == command[1]:
					break
			#server.transport.write(json.dumps({"response": ("call "+str(operator.getCall().getId())+" answered by operator "+str(operator.getId())+"\n")}).encode())
			my_json.append(json.dumps({"response": ("call "+str(operator.getCall().getId())+" answered by operator "+str(operator.getId()))}))
			#set state to busy
			operator.setState(switchState(2))
			operator.getCall().setState(switchCallState(2))

		case "reject":
			for operator in operators:
				if operator.getId() == command[1]:
					break
			#server.transport.write(json.dumps({"response": ("call "+str(operator.getCall().getId())+" rejected by operator "+str(operator.getId())+"\n")}).encode())
			my_json.append(json.dumps({"response": ("call "+str(operator.getCall().getId())+" rejected by operator "+str(operator.getId()))}))
			#operator available
			operator.setState(switchState(0))
			#remove call from the list
			for call in ongoingCalls:
				if call.getId() == operator.getCall().getId():
					calls.append(Call(call.getId()))
					ongoingCalls.remove(call)
					break

		case "hangup":
			#operator.setState(0)
			for operator in operators:
				if operator.getCall() != None \
					and operator.getCall().getId() == command[1]:
					break
			for call in calls:
				if call.getId() == command[1]:
					#server.transport.write(json.dumps({"response": ("call "+str(call.getId())+" missed\n")}).encode())
					my_json.append(json.dumps({"response": ("call "+str(call.getId())+" missed")}))
					calls.remove(call)
					missed = 1
			for call in ongoingCalls:
				if call.getId() == command[1] and call.getState() == switchState(1):
					#server.transport.write(json.dumps({"response": ("call "+str(call.getId())+" missed\n")}).encode())
					my_json.append(json.dumps({"response": ("call "+str(call.getId())+" missed")}))
					ongoingCalls.remove(call)
					operator.setState(switchState(0))
					operator.setCall(Call(None))
					missed = 1
			if not missed:
				#server.transport.write(json.dumps({"response": ("call "+str(operator.getCall().getId())+" finished and operator "+str(operator.getId())+" available\n")}).encode())
				my_json.append(json.dumps({"response": ("call "+str(operator.getCall().getId())+" finished and operator "+str(operator.getId())+" available")}))
				operator.setState(switchState(0))
				ongoingCalls.remove(operator.getCall())
				operator.setCall(Call(None))

	op = availableOperator(operators)
	#If there is a free operator
	#Call him, change the state and set the Operator
	if op and calls:
		#server.transport.write(json.dumps({"response": ("call " + str(calls[0].getId())+" ringing for operator "+ str(op.getId())+"\n")}).encode())
		my_json.append(json.dumps({"response": ("call " + str(calls[0].getId())+" ringing for operator "+ str(op.getId()))}))
		#give call to operator
		op.setCall(calls[0])
		#set state to ringing
		op.setState(switchState(1))
		#put it on the ongoing calls array
		ongoingCalls.append(calls[0])
		#set call to ringing
		calls[0].setState(switchCallState(1))
		#remove from the normal calls
		calls.remove(calls[0])
	if not op and calls:
		#server.transport.write(json.dumps({"response": ("call "+str(calls[-1].getId())+" waiting in queue\n")}).encode())
		my_json.append(json.dumps({"response": ("call "+str(calls[-1].getId())+" waiting in queue")}))
	server.transport.write(json.dumps(my_json).encode())
	return operator, calls, ongoingCalls
