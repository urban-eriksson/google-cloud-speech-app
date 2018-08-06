import re

# Base class for all state classes
class BaseState(object):

    # Some Utility functions for the indiviudal robot states

    def __init__(self):
        print('Processing current state: ' + str(self))
  
    def status_callback(self, data):
        if data['sender'] == 'Timer':
            print('>SM : Time left = ' + str(data['msg']) + 's')
            if data['msg'] == 0:
                brain.pub.publish('TimerZero')
                return InitState()
        return self

    def __repr__(self):
        # Leverages the __str__ method to describe the State.
        return self.__str__()

    def __str__(self):
        # Returns the name of the State.
        return self.__class__.__name__

 
class InitState(BaseState):

    def __init__(self):
        print('>SM : Entering state ' + str(self))
        self.text = 'Hi! Can you hear me?'
    # Waiting for the command from the master to begin
    def status_callback(self, data):
        if data['sender'] == 'Speech' and re.search(r'\b(yes|yeah)\b', data['payload'], re.I):
            return NameAsk()
        elif data['sender'] == 'Speech':
            self.text = 'Sorry, couldn''t get that. Let''s try again, can you hear me?'
            return self
        else:
            return super(InitState,self).status_callback(data)

class NameAsk(BaseState):

    def __init__(self):
        print('>SM : Entering state ' + str(self))
        self.text = 'Good! What''s your name?'

    def status_callback(self, data):
        if data['sender'] == 'Speech':
            return Greeting(data['payload']) 
        else:
            return super(NameAsk,self).status_callback(data)


class Greeting(BaseState):

    def __init__(self, name):
        print('>SM : Entering state ' + str(self))
        self.text = 'Hi' + name + '! Nice to meet you. Good bye.'

    def status_callback(self, data):
        if data['sender'] == 'Speech':
            return InitState() 
        else:
            return super(Greeting,self).status_callback(data)


class StateMachine(object):
    def __init__(self):

        # Start with a default state.
        self.state = InitState()
        #Timer 

    def status_callback(self, msg):
        #print 'Brain received: ' + msg.data
        sender,payload = msg.split(':')
        data = {'sender': sender, 'payload': payload}
        self.state = self.state.status_callback(data)

    def timer_callback(self, data):
        self.time -= 1
        data = {'sender':'Timer','payload':self.time}
        self.state = self.state.status_callback(data)


