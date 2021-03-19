#Library importing
from mpi4py import MPI
import time

#checking start time
start_time = time.time()

#Initialising Mpi4py and and getting number of threads
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print('rank',rank)

#creating data file object
file_in=open("smallTwitter.json")

#counter for number of rows processed on each thread
m=0

#loop to load and count the first line to be read by each thread
for i in range(0,rank-1):
    #skipping the lines read by other thread
    next(file_in)
a=file_in.readline()
m=m+1

#loop to load and count the lines to be read by each thread
while True:
    for i in range(1,size-1):
        #exception handeling as the file object could try to go past the last line
        try:
            #skipping the lines read by other thread
            next(file_in)
        except:
            break
    a=file_in.readline()
    if not a:
        break
    m=m+1

#closing the input file object
file_in.close()

#master thread gathering data from child nodes and integerating it
if rank == 0:
    s = 0
    for i in range(1,size):
        s=s+comm.recv()
    print(rank,":",s)
    print("--- %s seconds ---" % (time.time() - start_time))

#child threads sending the output of processed data
else:
    comm.send(m, dest=0)
    print(rank,":",m)
