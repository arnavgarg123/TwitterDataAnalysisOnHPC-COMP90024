#Library importing
from mpi4py import MPI
from collections import Counter
import time
import json
import sys

#checking start time
start_time = time.time()

# reading file name from command
data_file_nm = sys.argv[1]
map_file_nm = sys.argv[2]
sentiment_file_nm = sys.argv[3]


#Initialising Mpi4py and and getting number of threads
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print('Thread ',rank, 'started @', time.ctime())


#creating data file object
file_in=open(data_file_nm, encoding="utf8")
file_map=open(map_file_nm, encoding="utf8")
file_AFINN=open(sentiment_file_nm, encoding="utf8")

#List for sentiment data

############print(sentiment_word)

#loading melbourne geo data json file and extracting id and coordinates
map=json.load(file_map)
#dictionary for the coordinates
mapdict={}
for i in map['features']:
    mapdict[i['properties']['id']]=[i['properties']['xmin'],i['properties']['xmax'],i['properties']['ymin'],i['properties']['ymax']]

area_val_list=list(mapdict.values())
area_nm_list=list(mapdict.keys())
############print(mapdict)

#counter for number of rows processed on each thread
m=0
#counter for sentiment
total=[0 for i in range(len(mapdict))]

#skipping first line of file as we so not look at number of lines in the json file
next(file_in)
#loop to load and count the first line to be read by each thread
for i in range(0,rank):
    #skipping the lines read by other thread
    next(file_in)
a=file_in.readline()
#extracting text and coordinates from tweets
a=json.loads(a[:-2])
a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].lower().split()]

#counting sentiment score of a tweet, only if it lies in map range
#if flg_area==1:
#    result=fun()
#    total[j]+=sum(result)
    #counter
#    m=m+1

#loop to load and count the lines to be read by each thread
while True:
    for i in range(1,size):
        #exception handeling as the file object could try to go past the last line
        try:
            #skipping the lines read by other thread
            next(file_in)
        except:
            break
    a=file_in.readline()
        #counting sentiment score of a tweet, only if it lies in map range


#closing the input file object
file_in.close()

print("Tweets cnt by Area, Sum of Sentiments by Area= ")

#master thread gathering data from child nodes and integerating it
if rank == 0 or size==1:
    print("--- %s seconds ---" % (time.time() - start_time))

#child threads sending the output of processed data
else:
    print("Thread ", rank ," has shared data @", time.ctime())
