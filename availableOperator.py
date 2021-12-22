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

def availableOperator(operators):
	#print(operators[0].getState(), operators[1].getState())
	for operator in operators:
		if operator.getState() == switchState(0):
			return operator
	return 0
