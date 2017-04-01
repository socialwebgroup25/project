# Packages required
import csv


# List of possible mentions of parties
partyList = ['vvd','pvda','pvv','#SP',' sp ','cda','d66','christenunie','#cu','sgp','gl','groenlinks','pvdd','dieren','50plus','#denk','forum','fvd','piraten']


# List of actual party names
partyListName = ['VVD','PVDA','PVV','SP','CDA','D66','ChristenUnie','SGP','GroenLinks','Partij voor de Dieren','50Plus','DENK','Forum voor Democratie','Piratenpartij']


# List of parties that can get mentioned in multiple ways
doublesList = ['christenunie','#SP','gl','pvdd','forum']


# Function to read a .csv file
def readCsv(csvFile):
        with open(csvFile, 'rb') as myfile:
                data = myfile.readlines()
                tweetList = []
                requiredColumn = 4
                print('The data has length ' + str(len(data) - 1))

                for i in range(1,len(data)):
                        l = data[i].split(';')
                        if len(l) == 8:
                                tweetList.append(l[requiredColumn])
        return tweetList


def partyCount(tweets):
        # Enable entering both lists and filenames
        if (tweets[-4:-1] == '.cs'):
                tweets = readCsv(tweets)

        counter = [0] * len(partyList)
        partyCounted2 = []
        i = 0

        # Count the amount of mentions of parties in the list of parties
        for tweet in tweets:
                i = 0
                for party in partyList:
                        counter[i] += tweet.count(party)
                        i += 1

        partyCounted = zip(partyList,counter)
        
        # Combine the counts for the parties that get mentioned in different ways
        for i in range(len(partyListName)):
                if (partyCounted[i][0] in doublesList):
                        combinedCount = partyCounted[i][1] + partyCounted[i + 1][1]
                        partyCounted2.append((partyListName[i],combinedCount))
                        del partyCounted[i + 1]
                else:
                        partyCounted2.append((partyListName[i],partyCounted[i][1]))
                i += 1
        return partyCounted2

# Select file from which you want the parties to be counted
filename = 'full_14_maart_nobot.csv'
print partyCount(filename)

