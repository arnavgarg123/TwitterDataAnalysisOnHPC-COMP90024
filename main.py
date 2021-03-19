from mpi4py import MPI
import time
start_time = time.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print('rank',rank)
#print(size)
n=0
file_in=open("smallTwitter.json")
m=0
for i in range(0,rank-1):
    next(file_in)
a=file_in.readline()
m=m+1
#print(rank)
while True:
    for i in range(1,size-1):
        try:
            next(file_in)
        except:
            flag=1
    a=file_in.readline()
    if not a:
        flag=1
        break
    m=m+1
    #time.sleep(0.01)
file_in.close()

if rank == 0:
    s = 0
    for i in range(1,size):
        s=s+comm.recv()
    print(rank,":",s)
    print("--- %s seconds ---" % (time.time() - start_time))
    #comm.send(file_in.read(), dest=2)
else:
    comm.send(m, dest=0)
    print(rank,":",m)
    #print (s)
