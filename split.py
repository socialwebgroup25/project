# Import required packages

import csv
import time

# Set the time
start_time = time.time()

# Start with the vector containing the source, targets, change the csv file
# to the name of the file you want to import
# 
# Change filename to the filename you want to use

filename = "full_14_march.csv"
with open (filename, "r") as myfile:
    data=myfile.readlines()

# Makes two vectors from the imported data
def makevector(d):
    vector = []
    for i in range(len(d)):
        temp = d[i].split(";")
        e1 = temp[0]
        e2 = temp[1].rstrip()
        vector.append((e1,e2))
    return vector

# Select the name you want your output file to have
bestandsnaam = "gephi_14_march.csv"

# Simple function for checking whether x is larger than 1 or not
def larger1(x):
    return (x > 1)

# If vector is the vector of mentions run this to get a vector
# which tells if whe should split or not
def splitMentions(vector):
    sources = [i[0] for i in vector]
    targets = [i[1] for i in vector]

    targets2 = [(x.count(',')+1) for x in targets]
    for i in range(len(targets2)):
        if targets[i] == '':
            targets2[i] = 0
    needSplit = map(larger1,targets2)


    # Splitting all the values in the vector
    while (needSplit.count(True) > 0):
        splitloc = needSplit.index(True)
        mentions = (targets[splitloc]).split(",")
        mentions = filter(lambda a: a != '', mentions)
        n = len(mentions)
        for i in range(0,n):
            mention = mentions[i]
            vector.append((sources[splitloc],mention))
        vector.remove(vector[splitloc])
        sources = [i[0] for i in vector]
        targets = [i[1] for i in vector]
        
        targets2 = [(x.count(',')+1) for x in targets]
        for i in range(len(targets2)):
            if targets[i] == '':
                targets2[i] = 0
        needSplit = map(larger1,targets2)

    vector = zip(sources,targets)

    # Make self-loop if nobody is mentioned
    for i in range(len(vector)):
        if targets[i] == '':
            vector[i] = (sources[i],sources[i])
            
    return vector

# Function to write as csv file
def writeCsv(filename,v3):
    with open(filename,'wb') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['Source','Target'])
        for row in v3:
            csv_out.writerow(row)

v = makevector(data)
v2 = splitMentions(v)
writeCsv(bestandsnaam,v2)

# Show the time it took
print("--- %s seconds ---" % (time.time() - start_time))

