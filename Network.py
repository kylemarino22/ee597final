import random
from utils import *
import numpy as np
from Router import Router
from Packet import Packet

class Network():
    
    def __init__ (self):

        self.router_graph = []
        self.burst_on = True

    def generate_ticks (self, scale=3):
        # Set the scale to fit the ticks predominantly between 1 and 7
        ticks = abs(np.random.normal(loc=0, scale=scale))
        return int(round(ticks)) + 1

    def generate(self, N, density):
        
        
        self.router_graph = [Router(chr(65 + i)) for i in range(N)]
        
        self.sinkRouter = self.router_graph[-1]
        self.sinkRouter.sink = True
    
        # First create a simple graph to connect every node to the sink node.
        # Create a set of all unconnected nodes
        
        unconnected_nodes = set(self.router_graph[:-1])
        connected_nodes = {self.sinkRouter}
        
        links = []
        
        while len(unconnected_nodes) > 0:
            
            # Randomly select a connected node
            routerA = random.choice(list(connected_nodes))

            # Randomly select an unconnected node
            routerB = random.choice(list(unconnected_nodes))

            # Randomly determine etx and ticks
            etx = 1/random.uniform(0.5, 1)
            ticks = self.generate_ticks()

            # Create path from routerA to routerB
            routerA.createPath(routerB, etx, ticks)

            # Add both directions
            links.append((routerA.name, routerB.name))
            links.append((routerB.name, routerA.name))

            # Update sets of connected and unconnected nodes
            connected_nodes.add(routerB)
            unconnected_nodes.remove(routerB)
            
            
        # Once every node is connected, randomly make links until a desired 
        # density is reached. Since we're counting both paths in the link list,
        # we'll double the total_possible_connections
        total_possible_connections = N*(N-1)

        while len(links) < total_possible_connections * density:
            
            routerA = random.choice(self.router_graph)
            routerB = random.choice(self.router_graph)
            if routerA != routerB and (routerA.name, routerB.name) not in links:  # Ensure no duplicate or self-links
                etx = 1/random.uniform(0.5, 1)
                
                ticks = self.generate_ticks()
                routerA.createPath(routerB, etx, ticks)
                
                links.append((routerA.name, routerB.name))
                links.append((routerB.name, routerA.name)) 

                
    def set_sink(self, name):
        
        for router in self.router_graph:
            if router.name == name:
                self.sinkRouter = router
                self.sinkRouter.sink = True
                break
        
    def create_from_links(self, links):

        for a, b, etx, ticks in links:

            current_routers = [router.name for router in self.router_graph]

            if a not in current_routers:
                self.router_graph.append(Router(a))

            if b not in current_routers:
                self.router_graph.append(Router(b))

            # Find routers a and b in the graph, kinda sloppy method
            routerA = [router for router in self.router_graph if router.name == a][0]
            routerB = [router for router in self.router_graph if router.name == b][0]

            routerA.createPath(routerB, etx, ticks)
            
                    

    # Not constructor, used for initializing network with packets
    def init (self, init_states):

        # sinkRouterName = [router for router, state in init_states.items() if state[0] == 0][0]
        # sinkRouter = [router for router in self.router_graph if router.name == sinkRouterName][0] 
        # sinkRouter.sink = True 

        for routerName, (dummy_packets, data_packets) in init_states.items():
           router = [router for router in self.router_graph if router.name == routerName][0]
        #    router.queue = []
           router.queue.extend([Packet("dummy", 0) for _ in range(dummy_packets)])
           router.queue.extend([Packet("data", 0) for _ in range(data_packets)])
           
    
    def init_queue_grad (self):

        
        # Empty current packet and queues
        for router in self.router_graph:
            router.queue = []
            router.curr_packet = None
        
        # First need to create the dummy queue gradient
        initialized_nodes = {self.sinkRouter}
        uninitialized_nodes = set(self.router_graph)
        uninitialized_nodes.remove(self.sinkRouter)
        
        # print(uninitialized_nodes)

        while len(uninitialized_nodes) > 0:
            
            # For each uninitialized node, get all initialized nodes its connected to
            for uninit_node in list(uninitialized_nodes):
                
                routes = uninit_node.srcs + uninit_node.dests
                routers = [route[0] for route in routes]
                connected_initialized_nodes = {init_node for init_node in initialized_nodes if init_node in routers}

                # print(uninit_node.name)
                # print([route[0].name for route in routes])
                # print(connected_initialized_nodes)
                # print(self.sinkRouter in routes)

                # Skip if not connected to any nodes yet
                if len(connected_initialized_nodes) == 0:
                    continue

                # Get lowest queue size of connected initialized nodes
                min_queue_size = min([len(init_node.queue) for init_node in connected_initialized_nodes])

                print(uninit_node.name)
                uninit_node.queue = []
                uninit_node.queue.extend([Packet("dummy", 0) for _ in range(min_queue_size+1)])
                
                uninitialized_nodes.remove(uninit_node)
                initialized_nodes.add(uninit_node)

    def add_data(self, test_type, tick=0, scaling_factor=1):
        
        src_routers = [router for router in self.router_graph if router.sink == False]
        
        # Since dummy packets are 0 and data is 1, taking the sum gives the number of data packets!
        avaiable_capacity = sum([router.max_queue_size - sum([1 for packet in router.queue if packet.type == "data"]) for router in src_routers])
        max_capacity = sum([router.max_queue_size for router in src_routers])
        
        # print(avaiable_capacity, max_capacity, avaiable_capacity/max_capacity)
        
        if test_type == "BURSTY":
            # Randomly fill up queues to 90% capacity when on

            if self.burst_on:
                target_capacity = 0.7

                if avaiable_capacity/max_capacity > 0.60:
                    debugPrint(f"Burst Saturated at {tick}")
                    self.burst_on = False
                
            else:
                # target_capacity = 0
                
                if avaiable_capacity/max_capacity > 0.50:
                    debugPrint(f"Burst Emptied at {tick}")
                    self.burst_on = True
                    
                return

        elif test_type == "CONTINUOUS":
            # Randomly fill up queues to 70% capacity
            target_capacity = 0.7
            
        packets_to_add = int(avaiable_capacity * target_capacity * scaling_factor)

        available_routers = [router for router in src_routers if len(router.queue) < router.max_queue_size]

        if len(available_routers) == 0:
            return
        # print(available_routers)
            
        # Add packets randomly across the src_routers
        while packets_to_add > 0:
            router = random.choice(available_routers)
            router.queue.append(Packet("data", tick))
            packets_to_add -= 1
            # Exit the loop early if no more packets need to be added
            if packets_to_add <= 0:
                break
            