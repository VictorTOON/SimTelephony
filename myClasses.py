import enumerates

class Operator:
	_state = None
	_id = None
	_call = None

	def __init__(self, id):
		self.setState(enumerates.switchState(0))
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
		self.setState(enumerates.switchCallState(0))
		self.setId(id)

	def setState(self, new_state):
		self._state = new_state

	def getState(self):
		return self._state

	def setId(self, new_id):
		self._id = new_id

	def getId(self):
	 	return self._id
