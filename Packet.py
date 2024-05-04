from utils import *

class Packet():
    
    last_id = 0

    def __init__ (self, type, tick):
        self.type = type # Type can be "dummy" or "data"
        self.tx_progress = 0
        self.route = None
        self.start_tick = tick
        self.id = Packet.last_id + 1
        Packet.last_id += 1
        
    def print_route(self):
        
        debugPrint(f"Router {self.route[0].name}, ETX: {self.route[1]}, Ticks: {self.route[2]}, type: {self.type}")

    def __repr__ (self):
        
        return f"Packet(ID: {self.id}, Type: {self.type}, Progress: {self.tx_progress})"
