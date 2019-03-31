import random
from algorithm1 import algorithm1
#from algorithm2 import algorithm2

# Instead of on demand continuous broadcasting, we freeze the time and show the
# results in current time = 100
# We construct a sample list of requests that have arrived previously

broadcast_cycle = 20
current_time = 100 #sec
bandwidth = 100 #units/sec
items = []

#produce 2000 items stored in a list with the form : [id, size]
for i in range(2000):
    items.append([i,random.randint(30,200)])

#construct the request queue
def request_queue():
    requests = []
    #a request consists of:
    # id
    # deadline
    # arrival_time
    for i in range(100000):
        requests.append([random.randint(0,29), random.randint(20,60), random.randint(60,99)])

    return requests

#construct the pending queue with the form [id,size,deadline]
#a corresponding waiting time list is also constructed
def pending_queue(request_queue):
    pqueue = []
    item = []
    waiting_time = []

    for i in range(len(request_queue)):
        item.append(request_queue[i][0]) # id
        item.append(items[request_queue[i][0]][1]) # size
        item.append(request_queue[i][1]) # deadline
        pqueue.append(item)
        waiting_time.append(current_time - request_queue[i][2])
        item = []

    return pqueue, waiting_time

def main():

    #produce request queue randomly
    rq = request_queue()

    #produce pending queue and waiting_time
    pdq, waiting_time = pending_queue(rq)


    req_count = [] #number of requests for each item
    sizes = []

    all_req_ids = [] #temp list contains only the ids of the pending queue
    for i in range(len(pdq)):
    	all_req_ids.append(pdq[i][0])

    req_ids = [] #each item requested found once
    req_ids = set(all_req_ids)
    req_ids = list(req_ids)

    print("Item's of pending queue: ", req_ids)
    for i in req_ids:
        #count the requests of each item
        req_count.append(all_req_ids.count(i))

        #store the item's size
        sizes.append(items[i][1])

    reqs = []
    reqs.append(req_ids)
    reqs.append(req_count)
    reqs.append(sizes)


    #find waiting time of each request of d_i and store the oldest one
    waiting = []
    for i in range(len(reqs[0])):
        max = 0
        for j in range(len(pdq)):
            if reqs[0][i] == pdq[j][0]:
                if max < waiting_time[j]:
                    max = waiting_time[j]
        waiting.append(max)


    broadcast_queue = algorithm1(pdq, current_time, reqs, bandwidth, waiting, broadcast_cycle)
    print( "----------------------------------------------------------")
    print( broadcast_queue)
    print( "----------------------------------------------------------")

    #clustered_bcast_queue = algorithm2(broadcast_queue)
    #print (clustered_bcast_queue)

    # algorithm3()

main()
