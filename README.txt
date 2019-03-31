Papagatsia Maria 
Yfanti Sevasti

Channel Dynamic Adjustment in data broadcast

The paper consists of 3 algorithms:
1) S-RxW/SL algorithm : Evaluate the data item’s priority and select the data items broadcast in next cycle. 
2) WSAC algorithm: Cluster data items based on characteristics (weight,size).
3) CSDA algorithm: Split the original channel into sub-channels. Allocate data item into corresponding sub-channel.

The S-RxW/SL algorithm considers the request number of each item and its longest waiting time to evaluate the Weight directly. The data size and the request deadline are reflected by system loss SL. SL is the number of lost requests if the server broadcasts d_i at system time t.

We conducted a main.py where we run algorithm1.py (S-RxW/SL).
