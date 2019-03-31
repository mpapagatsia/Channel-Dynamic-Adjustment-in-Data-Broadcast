#The CSDA (Channel Splitting Data Allocation) Algorithm

def(bcast_queue, C):
    #bcast_queue = [list1: [id, size, deadline, weight], ...
    #               ....
    #               listn:  [id, size, deadline, weight], ...]
    sub_channels = []

    #sum size of BQ
    total_sum = 0
    for i in range(len(bcast_queue)):
        for j in range(bcast_queue[i]):
            total_sum += bcast_queue[i][j][1]


    for i in range(len(bcast_queue)):
        #bq(i) sum size
        bq_i_size = 0
        for j in range(bcast_queue[i]):
            bq_i_size += bcast_queue[i][j][1]

        temp_sc = bq_i_size / total_sum

        sub_channels.append(temp_sc)

    #schedule for broadcast with descending order of weight
    for i in range(len(bcast_queue)):
        weights = []
        for j in range(bcast_queue[i]):
            weights.append(bcast_queue[i][j][3])

        bcast_queue[i] = [d for _,d in sorted(zip(weights, bcast_queue[i]), reverse = True)]

        print("Channel " + i + "broadcasts list: " + bcast_queue[i])

    return sub_channels
