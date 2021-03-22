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

def fun():
    result=[]
    for x in sentiment_word:
        if len(x[:-1])>1:
            if " ".join(a[1]).count(" ".join(x[:-1]))>0:
                result=result+[int(x[-1])*" ".join(a[1]).count(" ".join(x[:-1]))]
                a[1]=" ".join(a[1]).replace(" ".join(x[:-1]),"123").split()
                #print("-----------",result, x[0])
        elif len(x[:-1])==1:
            if a[1].count(x[0])>0:
                result=result+[int(x[1])*a[1].count(x[0])]
    return result

#only run on child nodes
#if rank!=0 or size==1:
#creating data file object
file_in=open(data_file_nm, encoding="utf8")
file_map=open(map_file_nm, encoding="utf8")
file_AFINN=open(sentiment_file_nm, encoding="utf8")

#List for sentiment data
sentiment_word=[]
for i in file_AFINN.readlines():
    sentiment_word=sentiment_word+[i.replace("\n","").split()]
sentiment_word.sort(key=len,reverse=True)

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
a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].replace(",","").replace("!","").replace(".","").replace("?","").replace("'","").replace('''"''',"").lower().split()]

#calculating whether tweet lies in grids
flg_area=0
area_cnt = [0 for i in range(len(mapdict))]
for i in range(len(mapdict)):
    if (float(area_val_list[i][0]) <= float(a[0][0]) < float(area_val_list[i][1])) and (float(area_val_list[i][2]) <= float(a[0][1]) < float(area_val_list[i][3])):
        flg_area=1
        area_cnt[i]+=1
        j=i

#counting sentiment score of a tweet, only if it lies in map range
if flg_area==1:
    result=fun()
    total[j]+=sum(result)
    #counter
    m=m+1

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

    #last line is '''' }}\n '''' so we remove it
    if not a or a[:-1]=="]}":
        break
    #last json item does not end with comma
    if a[-2]==',':
        #extracting text and coordinates from tweets
        a=json.loads(a[:-2])
        a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].replace(",","").replace("!","").replace(".","").replace("?","").replace("'","").replace('''"''',"").lower().split()]


        #calculating whether tweet lies in grids
        flg_area=0
        for i in range(len(mapdict)):
            if (float(area_val_list[i][0]) <= float(a[0][0]) < float(area_val_list[i][1])) and (float(area_val_list[i][2]) <= float(a[0][1]) < float(area_val_list[i][3])):
                flg_area=1
                area_cnt[i]+=1
                j=i

        #counting sentiment score of a tweet, only if it lies in map range
        if flg_area==1:
            result=fun()
            total[j]+=sum(result)
            #counter
            m=m+1

    else:
        #extracting text and coordinates from tweets
        a=json.loads(a[:-1])
        a=[a["value"]["geometry"]["coordinates"],a["doc"]["text"].replace(",","").replace("!","").replace(".","").replace("?","").replace("'","").replace('''"''',"").lower().split()]

        # set_text=set(a[1])  redundant???

        #calculating whether tweet lies in grids
        flg_area=0
        for i in range(len(mapdict)):
            if (float(area_val_list[i][0]) <= float(a[0][0]) < float(area_val_list[i][1])) and (float(area_val_list[i][2]) <= float(a[0][1]) < float(area_val_list[i][3])):
                flg_area=1
                area_cnt[i]+=1
                j=i

        #counting sentiment score of a tweet, only if it lies in map range
        if flg_area==1:
            result=fun()
            total[j]+=sum(result)
            #counter
            m=m+1

#closing the input file object
file_in.close()
area_cnt_dict = {area_nm_list[i]: area_cnt[i] for i in range(len(mapdict))}
total_sent_dict = {area_nm_list[i]: total[i] for i in range(len(mapdict))}

#collecting data to be returned
to_be_sent=area_cnt_dict,total_sent_dict
print("Tweets cnt by Area, Sum of Sentiments by Area= ",to_be_sent)


#master thread gathering data from child nodes and integerating it
if rank == 0 or size==1:
    rcvd_val=0
    d1 = Counter(to_be_sent[0])
    d1 = {x:y for x,y in d1.items() if y!=0}
    d2 = Counter(to_be_sent[1])
    d2 = {x:y for x,y in d2.items() if y!=0}
    
    for i in range(1,size):
        rcvd_val=comm.recv()
        d1=Counter(d1)+Counter(rcvd_val[0])
        d2=Counter(d2)+Counter(rcvd_val[1])
    if rcvd_val:
        result = Counter({key : d2[key] / d1[key] for key in d1 if d1[key]!=0})
        print("Total Sentiment Score by Area:",d2)
        print("Tweets after Filtering by Area:",d1)
        print("Average sentiment Score by Area:",result)
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        d1 = Counter(to_be_sent[0])
        d1 = {x:y for x,y in d1.items() if y!=0}
        d2 = Counter(to_be_sent[1])
        d2 = {x:y for x,y in d2.items() if y!=0}
        result = Counter({key : d2[key] / d1[key] for key in d1 if d1[key]!=0})
        print("Total Sentiment Score by Area:",d2)
        print("Tweets after Filtering by Area:",d1)
        print("Average sentiment Score by Area:",result)
        print("--- %s seconds ---" % (time.time() - start_time))



#child threads sending the output of processed data
else:
    comm.send(to_be_sent, dest=0)
    print("Thread ", rank ," has shared data @", time.ctime())
