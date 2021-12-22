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
