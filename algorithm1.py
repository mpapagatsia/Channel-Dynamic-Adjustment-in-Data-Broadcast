#The S-RxW /SL algorithm


# reqs[ids,no_of_reqs,size_of_item]

def algorithm1(pq, t, reqs, bw, waiting_time, broadcast_cycle):
    b = []
    sl = []
    weight = []
    index = 0
    sumsize = 0

    #calculate SL
    for d in range(len(reqs[0])):
        temp = 0
        for k in pq:
            if k[0] != reqs[0][d]:
                if (k[2] + t) < (t + reqs[2][d]/bw):
                    temp = temp + 1
        sl.append(temp)

    #transform reqs list in order to use item's information in the form of a tuple
    final_list = []
    for i in range(len(reqs[0])):
        final_list.append([reqs[0][i], reqs[2][i]])

    #calculate weight
    for i in range(len(reqs[0])):
        if sl[i] != 0:
            temp_weight = reqs[1][i] * waiting_time[i] / sl[i]
        else:
            temp_weight = reqs[1][i] * waiting_time[i]

        #append on each item its weight
        weight.append(temp_weight)
        final_list[i].append(temp_weight)
        index = index + 1

    #sort the list of requests by descending order of the weights
    des_PQ = [d for _,d in sorted(zip(weight,final_list), reverse = True)]

    #select a list that fits in a broadcast cycle, the rest remains at pending queue
    for i in range(index):
        if sumsize < bw * broadcast_cycle:
            sumsize += des_PQ[i][1]
            b.append(des_PQ[i])

    return b
