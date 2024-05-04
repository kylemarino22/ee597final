from utils import *
import random

class Router():
    
    def __init__ (self, name):
       
       # Each link contains (router_pointer, ETX)
       self.name = name
       self.dests = [] 
       self.srcs = []
       self.max_queue_size = 10
       self.queue = []
       self.curr_packet = None
       self.penalty = 1
       self.sink = False
       
    def createPath (self, other, etx, ticks):

        self.dests.append((other, etx, ticks))
        other.srcs.append((self, etx, ticks))
        
    def getPacket(self, type):
        
        if len(self.queue) == 0:
            return None
        
        if type == "FIFO":
            return self.queue[0]

        elif type == "LIFO":
            return self.queue[-1]
        
    def removePacket(self, packet):
        try:
            self.queue.remove(packet)
        
        except ValueError:
            
            print(packet)
            print(self.queue)
            raise
            
    def sendPacket(self, packet):
    
        # Use BCP to determine next hop
        routes = self.dests + self.srcs
        
        best_route = -1
        best_weight = -100000
        for index, route in enumerate(routes):
            
            weight = (len(self.queue) - len(route[0].queue) - self.penalty*route[1])/route[2]

            if weight <= 0:
                continue
            
            if weight > best_weight:
                best_route = index
                best_weight = weight

        
        if best_route == -1:
            return False

        # Send packet
        packet.route = routes[best_route]
        debugPrint("Packet route: ", end='')
        packet.print_route() 

        self.curr_packet = packet

        
         
    def movePacket(self):

        packet = self.curr_packet
        dest_router = packet.route[0]
        debugPrint(f"Moving {packet} to {dest_router.name}")

        packet.tx_progress = 0

        # Determine using etx if packet made it successfully
        etx = packet.route[1]

        if random.random() < 1/etx:
            # Packet is successfully sent.
        
            self.removePacket(self.curr_packet)
            self.curr_packet = None
            
            if dest_router.sink == False:
                dest_router.queue.append(packet)
                return False, None
            else:
                return True, packet.start_tick
            
        return False, None

        
