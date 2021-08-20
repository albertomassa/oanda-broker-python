import json

class Account():
    def __init__(self, data):
        self.__dict__ = json.loads(data)

class Instrument(): 
    def __init__(self, data):
        self.__dict__ = json.loads(data)

class CandleStick():
    def __init__(self,data):
        self.__dict__ = json.loads(data)

    def getType(self):
        if(self.mid.get('o') == self.mid.get('c')):
            return 'NEUTRAL'
        elif(self.mid.get('o') > self.mid.get('c')):
            return 'BEAR'
        else:
            return 'BULL'

class Trade():
    def __init__(self,data):
        self.__dict__ = json.loads(data)

    def getState(self):
        if(float(self.unrealizedPL) > 0):
            return 'PROFIT'
        return 'LOSS'