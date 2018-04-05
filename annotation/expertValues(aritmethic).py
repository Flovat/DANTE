import csv
import os
from os.path import basename
import fileinput
import glob
import os.path
import itertools 


#da modificare
path_store = 'D:/Projects/DANTE/annotation/'
path_save = 'D:/Projects/DANTE/annotation/expert/'
path_videos = 'D:/Projects/DANTE/video/alpha/' 



def readValuesFromCSV(spamReader):
    frame = list()
    timestamp = list()
    value = list()
    csv_list = list()

    count = -1
    
    for row in spamReader:
        if (count==-1):
            frame.append('Frame')
        else:
            frame.append(count)    
        timestamp.append(row[0])
        value.append(row[4])
        count+=1

    csv_list.append(frame)
    csv_list.append(timestamp)
    csv_list.append(value)
    
    return len(frame), csv_list
        

def getExpertValues(video, value):
    values = list()
    valuesTmp = list()
    valuesAvg = list()
    frames = list()
    timestamps =list()
    dim = 0
    count = 0

    for annotator in os.listdir(path_store):
        if os.path.isdir(os.path.join(path_store, annotator)) and annotator!='expert':
            #print(annotator)
            
            for vid in os.listdir(path_store+annotator):
                

                if vid == video + '_mp4':
                    #print(vid)

                    path_name = path_store+annotator+'/'+vid+'/'+'valence.csv' if value == 'valence' else path_store+annotator+'/'+vid+'/'+'arousal.csv' 
                    if os.path.exists(path_name):
                        count+=1
                        #open file and extract values
                        with open(path_name, 'rt') as csvfile:
                                    spamReader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                    dim, csv_list = readValuesFromCSV(spamReader)
                                    tmp = csv_list[2]
                                    print((values))
                                    print((tmp))
                                    if not values:
                                        values = tmp
                                      
                                    else:
                                        
                                        for f,b in zip(values, tmp):
                                            if f!= 'Value' and b!= 'Value':
                                                valuesTmp.append(float(f)+float(b))
                                            else:
                                                valuesTmp.append("Value")
                                            
                                    print(valuesTmp)
                        
                        for i in valuesTmp:
                            if i == "Value":
                                valuesAvg.append(i)
                            else:
                                valuesAvg.append(i/count)   
                    
                        frames = csv_list[0]
                        timestamps = csv_list[1]
                              

                    else:
                        print('valori non esistenti per annotatore: ' + annotator)
                        if(count == 0): 
                            frames = []
                            timestamps = []
                            
    print((valuesAvg))                
    return dim, frames, timestamps, valuesAvg     
   

    

                                    
                                    

def writeValuesCSV(videoName, dim, csv_list, value):   
    path = path_save + 'expert_valence_' + videoName + '.csv' if value=='valence' else path_save + 'expert_arousal_' + videoName + '.csv'
    with open(path, 'w') as outfile:
        
        for i in range(0, dim):
            k=0
            for entries in csv_list:
                if k!=0:
                    outfile.write(';')  
                   
                outfile.write(str(entries[i]))
                k+=1
            outfile.write('\n')

            
                                

def main():

    videos = list()
    
  
    for video in os.listdir(path_videos):

        valence = list()
        arousal = list()
        csv_listV = list()
        csv_listA = list()

        if os.path.join(path_videos, video) != os.path.join(path_videos, 'Example.mp4'):
        
            #print(video)
            #estraggo solo il file name senza estensione
            base = (basename(video))
            videoName = os.path.splitext(base)[0]
            
            print(videoName)
           
            #calcolo valence di ogni video
       
            print('....is writing valence')

            dimV, frameV, timestampV, valence = getExpertValues(videoName, 'valence')
            if dimV !=0 and frameV != [] and timestampV != [] and valence != []:
                csv_listV.append(frameV)
                csv_listV.append(timestampV)
                csv_listV.append(valence)
                writeValuesCSV(videoName, dimV, csv_listV, 'valence')
            else:
                print('non scrivo i valori')
            
            
            
            print('.....is writing arousal')
            dimA, frameA, timestampA, arousal = getExpertValues(videoName, 'arousal')
            if dimA !=0 and frameA != [] and timestampA != [] and arousal != []:
                csv_listA.append(frameA)
                csv_listA.append(timestampA)
                csv_listA.append(arousal)
                writeValuesCSV(videoName, dimA, csv_listA, 'arousal')
            else:
                print('non scrivo i valori')
                
           
            



main()  