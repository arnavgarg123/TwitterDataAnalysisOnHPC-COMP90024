#Library importing
from mpi4py import MPI
import time
import json

#checking start time
start_time = time.time()

#Initialising Mpi4py and and getting number of threads
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print('rank',rank)

#only run on child nodes
if rank!=0 or size==1:
    #creating data file object
    file_in=open("bigTwitter.json", encoding="utf8")
    file_map=open("melbGrid.json", encoding="utf8")
    file_AFINN=open("AFINN.txt", encoding="utf8")

    #List for sentiment data
    sentiment_word=[]
    for i in file_AFINN.readlines():
        sentiment_word=sentiment_word+[i.replace("\n","").split("\t")]
    ############print(sentiment_word)

    #loading melbourne geo data json file and extracting id and coordinates
    map=json.load(file_map)
    #dictionary for the coordinates
    mapdict={}
    for i in map['features']:
        mapdict[i['properties']['id']]=[i['properties']['xmin'],i['properties']['xmax'],i['properties']['ymin'],i['properties']['ymax']]
    ############print(mapdict)

    #counter for number of rows processed on each thread
    m=0
    #counter for sentiment
    total=0

    #skipping first line of file as we so not look at number of lines in the json file
    next(file_in)
    #loop to load and count the first line to be read by each thread
    for i in range(0,rank-1):
        #skipping the lines read by other thread
        next(file_in)
    a=file_in.readline()
    #extracting text and coordinates from tweets
    a=json.loads(a[:-2])
    a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].replace(",","").replace("!","").replace(".","").replace("?","").replace("'","").replace('''"''',"").lower().split()]

    #counting sentiment score of a tweet
    result = [int(x[1])*a[1].count(x[0]) for x in sentiment_word if a[1].count(x[0])>0]
    total=total+sum(result)
    #print("Total = ",total)

    #counter
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

        #last line is '''' }}\n '''' so we remove it
        if not a or a[:-1]=="]}":
            break
        #last json item does not end with comma
        if a[-2]==',':
            #extracting text and coordinates from tweets
            a=json.loads(a[:-2])
            a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].replace(",","").replace("!","").replace(".","").replace("?","").replace("'","").replace('''"''',"").lower().split()]

            #counting sentiment score of a tweet
            result = [int(x[1])*a[1].count(x[0]) for x in sentiment_word if a[1].count(x[0])>0]
            #print(result)
            total=total+sum(result)
        else:
            #extracting text and coordinates from tweets
            a=json.loads(a[:-1])
            a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].replace(",","").replace("!","").replace(".","").replace("?","").replace("'","").replace('''"''',"").lower().split()]

            set_text=set(a[1])
            result = [int(x[1])*a[1].count(x[0]) for x in sentiment_word if a[1].count(x[0])>0]
            total=total+sum(result)

        #counter
        m=m+1

    #closing the input file object
    file_in.close()
    print("Total = ",total)
#master thread gathering data from child nodes and integerating it
if rank == 0 or size==1:
    s = 0
    for i in range(1,size):
        s=s+comm.recv()
    if s:
        print(rank,":",s)
    else:
        print(rank,":",m)
    print("--- %s seconds ---" % (time.time() - start_time))

#child threads sending the output of processed data
else:
    comm.send(m, dest=0)
    print(rank,":",m)
