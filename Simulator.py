from Packet import Packet
from utils import *

def init_packets(router_graph):
    # Ensure each router's current packet is set to None
    for router in router_graph:
        router.curr_packet = None

    # Initially fill network with dummy packets to create queue gradient
    router_graph[0].queue = [Packet("dummy") for _ in range(3)]
    router_graph[1].queue = [Packet("dummy") for _ in range(2)]
    router_graph[2].queue = [Packet("dummy") for _ in range(1)]
    router_graph[3].queue = []

    # Inject network with real data packets
    router_graph[1].queue.extend([Packet("data") for _ in range(3)])
    router_graph[2].queue.extend([Packet("data") for _ in range(3)])

    
def update_routers(router_graph):
    """Simulate router updates for one timestep."""
    snapshot = []
    for router in router_graph:
        if router.curr_packet is None:
            tx_packet = router.getPacket("FIFO")
            router.sendPacket(tx_packet)

        router.curr_packet.tx_progress += 1
        if router.curr_packet.tx_progress == router.curr_packet.route[2]:
            router.movePacket(tx_packet)
        
        # Take a snapshot of the queue at the current state
        snapshot.append([(1 if pkt.type == 'data' else 0) for pkt in router.queue])
    return snapshot

    
def eval_bcp(network, tick, latencies, snapshots=None, queue_type="LIFO"):

    if snapshots is not None:
        snapshot = {} 

        # Record packets at the start of an iteration    
        for router in network.router_graph:  
            snapshot[router.name] = [(1 if pkt.type == 'data' else 0) for pkt in router.queue]

        snapshots.append(snapshot)

        debugPrint(snapshots)
        
        
    pckts_recvd = 0

    # Ok so I need to measure throughput and latency. Throughput will just be
    # the total number of packets that make it to the sink. Latency will be the total
    # number of ticks it takes for a packet to get to the sink. I need to add an 
    # initial tick to the packet and ending tick to measure how long it takes. 

    # Increment by a single tick
    for router in network.router_graph:
        
        debugPrint(f"Decision Phase Router: {router.name}")

        if router.curr_packet == None:
        
            # Using fifo method
            tx_packet = router.getPacket(queue_type)
            
            debugPrint(f"Next packet for router to send: {tx_packet}")

            if tx_packet is None:
                continue
            
            # Decides packet destination
            router.sendPacket(tx_packet)
            
        if router.curr_packet is None:
            continue 
        
        router.curr_packet.tx_progress += 1
        
    debugPrint("====")
        
    for router in network.router_graph:
        
        if router.curr_packet is None:
            continue
            
        debugPrint(f"Send Phase Router: {router.name}")

        if router.curr_packet.tx_progress == router.curr_packet.route[2]:
            
            # Move packet to next router
            reached_sink, start_tick = router.movePacket()

            #TODO increment total count
            if reached_sink:
                latencies.append(tick-start_tick)
                pckts_recvd += 1

    return pckts_recvd