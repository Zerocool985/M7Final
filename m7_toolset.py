import pandas as pd
import csv

gerMonthNames = {
        "Januar" : 1,
        "Februar" : 2,
        "März" : 3,
        "April" : 4,
        "Mai" : 5,
        "Juni" : 6,
        "Juli" : 7,
        "August" : 8,
        "September" : 9,
        "Oktober" : 10,
        "November" : 11,
        "Dezember" : 12
    }

def getGenesisData(filename, headerRowBot, headerRowTop):
    the_file = open(filename, 'r')
    reader = csv.reader(the_file)
    
    #read headers
    headerCount=headerRowTop-headerRowBot
    headerRowBot=headerRowBot-2 #QOL for the user input when calling the function
    i = 0
    headerlist=[]
    finallist=[]
    for row in reader:
        if i > headerRowBot and i < headerRowTop:
            headerlist.append(row)
        if i>headerRowTop:
            break
        i=i+1

    the_file.close()
    for idx, lists in enumerate(headerlist):
        headerlist[idx]=lists[0].split(";")

    #Dynamic Header String
    for idx, line in enumerate(headerlist[0]):
        string=""
        for i in range(len(headerlist)-1):
            string=string +"/" +headerlist[i][idx]
        string = string + "/" +headerlist[len(headerlist)-1][idx]
        while string[0]=="/": # cut of leading "/" on single line headers
            string = string[1:]

        finallist.append(string)   

    #build DataFrame
    df=pd.read_csv(filename,encoding="latin-1", sep=";", header=headerRowTop-1)
    df.columns = df.columns[:0].tolist() + finallist
    #drop everthing after "__________" (Copyright, etc.) 
    df=df.drop(range(df.loc[df.iloc[:,0] == "__________"].index.values.astype(int)[0],df.shape[0]))


    monthCol=-1
    yearCol=-1
    dayCol=-1
    #print(headerlist)
    #define Types
    for idx, line in enumerate(headerlist[headerCount]):
    #get Time Columns:
        if line== "Monat":
            monthCol=idx
            df[df.columns[idx]].replace(gerMonthNames, inplace=True)
        if line == "Jahr":
            yearCol=idx
            df[df.columns[idx]] = pd.to_numeric(df[df.columns[idx]], errors='coerce')
        if line == "Stichtag":
            dayCol=idx
    #Numeric: 
#If some values in column are missing (NaN) and then converted to numeric, always dtype is float. You cannot convert values to int. Only to float, because type of NaN is float.
        if (line =="Anzahl" or line == "1000 cbm" or line== "Tsd. EUR" #ergänzen aller Fälle
            or line == "1000 qm"
           ): 
            df[df.columns[idx]] = pd.to_numeric(df[df.columns[idx]], errors='coerce')
        #else:
            #df[df.columns[idx]] = pd.Categorical(df[df.columns[idx]])
    #create Time column from Year/Month/Day
    if monthCol!=-1 and yearCol!=-1:
        df["Date"]=pd.to_datetime(df.Jahr*10000+df.Monat*100+1.0,format='%Y%m%d')
    if monthCol==-1 and yearCol!=-1:
        df["Date"]=pd.to_datetime(df.Jahr*10000+1.0*100+1.0,format='%Y%m%d')

    return df