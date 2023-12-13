Run the simulation with:
python scheduling.py <qlist> <T> <c_t> <Edges> <latency> <frequency> <processorinfo> <c_p> 

<qlist> is the priority list
<T> is the execution time of each task on each processor
<c_t> is the communication cost between tasks
<Edges> is the matrix that show the edges between tasks
<latency> is the threshold set for DUPRS part 1 and part 2
<frequency> is the frequency information of the processors
<processorinfo> is the infomation of the processors needed for calculation the engery consumption with equation (7) 
<c_p> is the communication factor between processors 

An example of runnning the simulation is:
python scheduling2.py "[1,2,3,4,5,6,7,8,9,10]" "[[7,14,25],[16,19,14],[11,20,24],[18,12,20],[9,20,13],[11,20,23],[14,18,8],[16,19,21],[11,17,20],[13,14,11]]" "[[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1]]" "[[0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,1,0,1,0,1,0,0,0,0],[0,1,0,1,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,0]]" "1000" "[[0.5,1.0],[0.5,1.0],[0.6,1.0]]" "[[0.03,0.8,2.9],[0.04,0.8,2.5],[0.07,1.0,2.5]]" "[[0,1,1],[1,0,1],[1,1,0]]" 
