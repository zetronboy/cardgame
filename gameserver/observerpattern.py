#!/usr/bin/env python3

#observer pattern
#notify object when another wishes to share data or sync state
from abc import ABCMeta,abstractmethod
TRACE=False #verbose object trace
SPY=False #show all state change values in console

class ObservableBase(metaclass=ABCMeta):
	"""
	Know its observers. Any number of Observer objects may observe a
	subject.
	Send a notification (update) with a observed_state object to its observers when its state changes.
	use attach and detach to subscribe
	"""

	_observers = set()
	if TRACE: print("Observerable created") 
	_subject_state = None

	def attach(self, observer):
		observer._subject = self
		self._observers.add(observer)

	def detach(self, observer):
		observer._subject = None
		self._observers.discard(observer)

	def _notify(self):
		for observer in self._observers:
			observer.update(self._subject_state)
			if TRACE: print("Notified an observer")

	@property
	def state(self): #a getter
		return self._subject_state

	@state.setter
	def state(self, arg):
		self._subject_state = arg
		if TRACE: print("State changed, sending notify")
		if SPY: print("Notify '{}'".format(arg))
		self._notify()
		

class ObserverBase(metaclass=ABCMeta):
	"""
	Define an updating interface for objects that should be notified of
	changes in a subject.
	"""

	_subject = None
	_observer_state = None
	if TRACE: print("Overserver created")

	@abstractmethod
	def update(self, arg):
		pass


class ConcreteSubject(ObservableBase):
	def __init__(self):
		if TRACE: print("ConcreteSubject initialized")

	def changeState(self):
		if TRACE: print("Changing state")
		self.state="you have been notified"


class ConcreteObserver(ObserverBase):
	"""
	Implement the Observer updating interface to keep its state
	consistent with the subject's.
	Store state that should stay consistent with the subject's.
	"""
	def __init__(self):
		if TRACE: print("ConcreteObserver initialized")

	def update(self, arg): #override base
		self._observer_state = arg
		if TRACE: print("observed a state change of '{}'".format(arg))
		

def main():
	subject = ConcreteSubject()
	concrete_observer = ConcreteObserver()
	subject.attach(concrete_observer)
	subject.changeState()


if __name__ == "__main__":
	main()
