#Using Pyhton 3.10
def switchState(MyState):
	switcherState = {
		0: "available",
		1: "ringing",
		2: "busy"
	}
	return switcherState.get(MyState)

def switchCallState(MyCallState):
	switcherCallState = {
		0: "received",
		1: "ringing",
		2: "answered",
		3: "rejected",
	}
	return switcherCallState.get(MyCallState)

class Operator:
	_state = None
	_id = None
	_call = None

	def __init__(self, id):
		self.setState(switchState(0))
		self.setId(id)

	def setState(self, new_state):
		self._state = new_state

	def getState(self):
		return self._state

	def setId(self, new_id):
		self._id = new_id

	def getId(self):
	 	return self._id

	def getCall(self):
		return self._call

	def setCall(self, new_call):
		self._call =  new_call

class Call:
	_state = None
	_id = None

	def __init__(self, id):
		self.setState(switchCallState(0))
		self.setId(id)

	def setState(self, new_state):
		self._state = new_state

	def getState(self):
		return self._state

	def setId(self, new_id):
		self._id = new_id

	def getId(self):
	 	return self._id


command = ["default"]
operator = "default"
calls = []
ongoingCalls = []

#creating operators, could be a list
operatorA = Operator("A")
operatorB = Operator("B")

operators = [operatorA, operatorB]

def availableOperator(operators):
	#print(operators[0].getState(), operators[1].getState())
	for operator in operators:
		if operator.getState() == switchState(0):
			return operator
	return 0

while(command[0] != "exit"):
	missed = 0
	#list of commands to be called
	command = (input().split())
	#for every command and ID in the list, checks everything
	match command[0]:
		case "call":
			print("call",command[1],"received")
			#creates a call with an id
			calls.append(Call(command[1]))

		case "answer":
			#find operator
			for operator in operators:
				if operator.getId() == command[1]:
					break
			print("call",operator.getCall().getId(),"answered by operator",operator.getId())
			#set state to busy
			operator.setState(switchState(2))
			operator.getCall().setState(switchCallState(2))

		case "reject":
			for operator in operators:
				if operator.getId() == command[1]:
					break
			print("call",operator.getCall().getId(),"rejected by operator",operator.getId())
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
					print("call", call.getId(), "missed")
					calls.remove(call)
					missed = 1
			for call in ongoingCalls:
				if call.getId() == command[1] and call.getState() == switchState(1):
					print("call", call.getId(), "missed")
					ongoingCalls.remove(call)
					operator.setState(switchState(0))
					operator.setCall(Call(None))
					missed = 1
			if not missed:
				print("call",operator.getCall().getId(),"finished and operator",operator.getId(),"available")
				operator.setState(switchState(0))
				ongoingCalls.remove(operator.getCall())
				operator.setCall(Call(None))

	op = availableOperator(operators)
	#If there is a free operator
	#Call him, change the state and set the Operator
	if op and calls:
		print("call",calls[0].getId(),"ringing for operator",op.getId())
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
		print("call",calls[-1].getId(),"waiting in queue")
