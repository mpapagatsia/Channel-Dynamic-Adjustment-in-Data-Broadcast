#The WSAC (Weight Size Average Clustering) algorithm
from numpy import array
from numpy import linalg as LA
from sklearn.model_selection import KFold
from sklearn.cluster import KMeans
from collections import Counter
from random import random, choice

#b here is the sub-queue of b
def algorithm2(b):
    bcast_queue = []

    #Part 1
    #clustering by column 3 (Weight)
    set_by_weight = kodama(b, 2)

    print("!) set_by_weight= ", set_by_weight)
    #calculate avg weight for each s[i]
    avg_weight = []
    for key in set_by_weight:
        temp = 0
        print("key = ", key)
        for j in range(len(set_by_weight[key])):
            temp += set_by_weight[key][j][2]
        temp = temp / float(len(set_by_weight[key]))
        avg_weight.append((key,temp))

    print("avg_weight ", avg_weight)
    print("-------------------------------------------------")
    print("-------------------------------------------------")
    print("set_by_weight= ", set_by_weight)
    print("-------------------------------------------------")
    print("-------------------------------------------------")
    #check the order!!!!!!!!!!!!!!
    #Schedule lists by weight's desending order
    des_weight = [d for _,d in sorted(zip(avg_weight,set_by_weight), reverse = True)]

    #print(set_by_weight[des_weight[0]])
    #Part 2
    #clustering each sub-list by size. column 1
    set_by_size_weight = []
    avg_size = []
    final_clustering = []
    print("----------------------------------------------")
    for i in range(len(des_weight)):
        #print("*****************************")
        #print("set_by_weight[des_weight[i]]= ", set_by_weight[des_weight[i]])
        #print("*****************************")
        set_by_size_weight.append(kodama(set_by_weight[des_weight[i]], 1))
        #print("set_by_size_weight = ", set_by_size_weight)
        #calculate avg size for each s[i][j]

        for key in set_by_size_weight[i]:
            temp = 0
            #print("set_by_size_weight[key]= ",set_by_size_weight[i][key])
            for j in range(len(set_by_size_weight[i][key])):
                temp += set_by_size_weight[i][key][j][2]
            temp = temp / float(len(set_by_size_weight[i][key]))
            avg_size.append(temp)


        #Schedule lists by size's desending order
        des_size_weight = [d for _,d in sorted(zip(avg_size,set_by_size_weight[i]), reverse = True)]
        final_clustering.append(set_by_size_weight[i][des_size_weight[0]])

    #Part 3
    print("----------------------------------------------")
    print("final clustering= ", final_clustering)
    #find the max dimentions in order to equalize them
    max_lists = max(final_clustering,key=len)

    max_objects = max(final_clustering[0], key=len)
    for i in range(1,len(final_clustering)):
        max_i = max(final_clustering[i], key=len)
        if max_i > max_objects:
            max_objects = max_i

    #fill the lists with empty slots

    for i in range(len(final_clustering)):
        if len(final_clustering[i]) < max_lists:
            for i in range(max_lists - len(final_clustering[i])):
                final_clustering[i].append([])

    for i in range(len(final_clustering)):
        for j in range(max_lists):
            if len(final_clustering[i][j]) < max_objects:
                for k in range(max_objects - len(final_clustering[i][j])):
                    final_clustering[i][j].append([])


    #Build the Broadcast Queue
    for i in range(len(max_lists)):
        temp = []
        for j in range(max_objects):
            for k in range(final_clustering):
                if final_clustering[k][i][j] != []:
                    temp.append(final_clustering[k][i][j])

        bcast_queue.append(temp)
    return bcast_queue


def optimal_k_strategy(characteristic):
    k = len(characteristic) #number of clusters = number of samples
    omega = characteristic #either weights or size
    #print("k= ",k)
    #print("characteristic= ", characteristic)

    while(True):
        #calculate the average inter - cluster dissimilarity
        a_k = k * (k-1)
        #for i in range(k):
        #    a_k += k - i -1
        dist = 0
        for i in range(k):
            for j in range(k):
                dist += abs(characteristic[i] - characteristic[j]) ** 2 #distance of weights

        d = dist / (a_k**2)
        #print("d= ", d)
        i = 0
        changes = 0
        while True :
            j = 0
            while True :
                #print("--k= , j= ", k, j)
                if i != j:
                    d_inter = abs (omega[i] - omega[j]) ** 2
                    if d_inter < d / 2:
                        omega[i] = (omega[i] + omega[j]) / 2
                        k -= 1
                        del omega[j]
                        changes = 1
                    else:
                        j += 1
                else:
                    j += 1
                if j >= k:
                    break

            i += 1
            if i >= k:
                break


        if not changes :
            break

    return k

def kodama(b, attr):
    MAX_ITER = 20 # number decided by paper [29]
    #construct the indicator vector T
    #each T[i] contains the attribute value of d[i] item

    T = []
    for i in range(len(b)):
        T.append(b[i][attr])

    length = len(T)
    if length == 1 :
        sets = {T[0]:[b[0]]}
        return sets

    k = optimal_k_strategy(T)

    if length == k:
        sets = {}
        #print("keys ", keys)
        for i in range(length):
            sets.update({T[i]:[b[i]]})

        return sets
    #10-fold CV

    # if # of samples is less than the number of chunks (10 defined by the paper)
    # then we assume:

    if length < 10:

        splitting = length
    else:
        splitting = 10

    kfold = KFold(splitting, True, 1)

    z_t = [] #record of the predicted class labels for each sample

    T = []
    for i in range(len(b)):
        T.append(b[i][attr])

    for train, test in kfold.split(T):
        #print("-------------")
        train_set = []
        test_set = []
        for i in range(len(train)):
            train_set.append(T[train[i]])
            #print('train: %s' % (d[train[i]]))
        for i in range(len(test)):
            test_set.append(T[test[i]])
            #print('test: %s' % (d[test[i]]))

        train_set = array(train_set).reshape(-1,1)
        test_set = array(test_set).reshape(-1,1)
        """print("train_set ", train_set)
        print(" k=", k)
        print("test_set ", test_set)
        print("train_set shape ", train_set.shape)
        print("test_set shape ", test_set.shape)"""
        kmeans = KMeans(n_clusters=k, random_state=0).fit(train_set)
        #print(kmeans.labels_)
        #print(kmeans.cluster_centers_)

        prediction = kmeans.predict(test_set)
        #print("prediction= ", prediction)
        #print("test_set ", test_set)
        #print("test_set 0 ", test_set[0][0])
        for i in range(len(prediction)):

            z_t.append((test_set[i][0],T[prediction[i]]))
            #print("z_t= ", z_t)


    #print("z_t = ", z_t)
    #for i in range(len(z)):
    #    print(z[i])

    accuracy_t = 0
    V = []
    for i in range(len(T)):

        if T[i] == z_t[i][1]:
            V.append(z_t[i][1])
            accuracy_t += 1
        else:
            temp_list = [i[1] for i in z_t]
            while True:
                swap = choice(temp_list)
                if z_t[i][1] != swap:
                    V.append(swap)
                    break


    temp = float(len(T))
    accuracy_t = accuracy_t / temp


    for j in range(MAX_ITER):
        #second k-fold and kmeans for vector V
        kfold = KFold(splitting, True, 1)

        z_v = [] #record of the predicted class labels for each sample

        for train, test in kfold.split(V):
            #print("-------------")
            train_set = []
            test_set = []
            for i in range(len(train)):
                train_set.append(V[train[i]])
                #print('train: %s' % (d[train[i]]))
            for i in range(len(test)):
                test_set.append(V[test[i]])
                #print('test: %s' % (d[test[i]]))

            train_set = array(train_set).reshape(-1,1)
            test_set = array(test_set).reshape(-1,1)

            #kmeans = KMeans(n_clusters=k, random_state=0).fit(train_set)
            #print(kmeans.labels_)
            #print(kmeans.cluster_centers_)

            prediction = kmeans.predict(test_set)


            for i in range(len(prediction)):
                z_v.append((test_set[i][0],T[prediction[i]]))


        #print("z_v = ", z_v)
        #for i in range(len(z)):
        #    print(z[i])

        accuracy_v = 0
        for i in range(len(V)):

            if V[i] == z_v[i][1]:
                accuracy_v += 1


        accuracy_v = accuracy_v / temp

        if accuracy_v > accuracy_t:
            accuracy_t = accuracy_v
            T = V.copy()
            z_t = z_v.copy()

            #Construct V list again
            V = []
            for i in range(len(T)):

                if T[i] == z_t[i][1]:
                    V.append(z_t[i][1])

                else:
                    temp_list = [i[1] for i in z_t]
                    while True:
                        swap = choice(temp_list)
                        if z_t[i][1] != swap:
                            V.append(swap)
                            break


        elif accuracy_t == accuracy_v:
            break

    #print("-------------------------------------")
    #print("T= ", T)

    print("-------------------------------------")
    print("z_t= ", z_t)

    temp_list = [i[1] for i in z_t]
    keys = set(temp_list)
    keys = list(keys)
    #s = set( val for dic in lis for val in dic.values())
    sets = {}
    #print("keys ", keys)
    for i in range(len(keys)):
        sets.update({keys[i]:[]})

    for i in range(len(keys)):
        for j in range(len(z_t)):
            if keys[i] == z_t[j][1]:
                for k in range(len(T)):
                    if z_t[j][0] == T[k]:

                        sets[keys[i]].append(b[k])
                        break

    return sets # returns a dictionary with the subsets of b list clustered by attribute
