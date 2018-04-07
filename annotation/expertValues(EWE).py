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

    #parto da -1 perché il primo valore voglio che sia la stringa nome della colonna 
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

def readValuesFromExpert(file, spamReader):
    valuesExpert = list()
    for row in spamReader:
        valuesExpert.append(row[2])
 
    return valuesExpert


def calculateEWE(dictExpertCoeff, video, dim, value):

    N = 0
    D = 0
    valuesAvg = list()
    valuesAvg.append("Value")
    #print("dim",dim, "video", video)
    for i in range(1,dim-1):
        #ciclo per tutti gli annotatori che non sono l'esperto
        for annotator in os.listdir(path_store):
            if os.path.isdir(os.path.join(path_store, annotator)) and annotator!='expert':

                #ciclo su tutti i video di quell'annotatore
                for vid in os.listdir(path_store+annotator):
                    #se esiste
                    base = (basename(video))
                    videoName = os.path.splitext(base)[0]

                    if vid == videoName + '_mp4':
                        
                        #cambia a seconda se è valence o arousal
                        path_name = path_store+annotator+'/'+vid+'/'+'valence.csv' if value == 'valence' else path_store+annotator+'/'+vid+'/'+'arousal.csv'
                        if os.path.exists(path_name):
                            #print('\nvalori esistenti per annotatore: ' + annotator)
                            
                            
                            #open file and extract values
                            with open(path_name, 'rt') as csvfile:
                                        spamReader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                        dim, csv_list = readValuesFromCSV(spamReader)
                                        tmp = csv_list[2]
                                        #print(dictExpertCoeff.get(annotator))
                                        #print(i)
                                        print("len",len(tmp), annotator, i)
                                        N += float(tmp[i]) * float(abs(dictExpertCoeff.get(annotator)))
                                        D += abs(dictExpertCoeff.get(annotator))
                                        
        valuesAvg.append(float(N)/float(D))
        
    #print(valuesAvg)
    return valuesAvg
    
                                        
                                    
                        



def getExpertValues(video, value):
    values = list()
    valuesTmp = list()
    valuesAvg = list()
    valueDiffExpert = 0
    dim = 0
    count = 0
    frames = list()
    timestamps = list()
    dictExpertCoeff = {}

    file = 'expert_'+ value + '_' + video + '.csv'                             
    if (os.path.exists(path_save+file)):
        print('esperto trovato')
        #open file and extract values
        with open(path_save + file, 'rt') as csvfile:
            spamReaderExpert = csv.reader(csvfile, delimiter=';', quotechar='|')
            values = readValuesFromExpert(file, spamReaderExpert)
            #print('Expert',  values)
    else:
        print('esperto NON trovato')

    #ciclo per tutti gli annotatori che non sono l'esperto
    for annotator in os.listdir(path_store):
        if os.path.isdir(os.path.join(path_store, annotator)) and annotator!='expert':
            #ciclo su tutti i video di quell'annotatore
            for vid in os.listdir(path_store+annotator):
                #se esiste
                if vid == video + '_mp4':
                    #cambia a seconda se è valence o arousal
                    path_name = path_store+annotator+'/'+vid+'/'+'valence.csv' if value == 'valence' else path_store+annotator+'/'+vid+'/'+'arousal.csv'
                    if os.path.exists(path_name):
                        #print('\nvalori esistenti per annotatore: ' + annotator)
                        count += 1
                        
                        #open file and extract values
                        with open(path_name, 'rt') as csvfile:
                                    spamReader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                    dim, csv_list = readValuesFromCSV(spamReader)
                                    tmp = csv_list[2]
                            
                                    if (not os.path.exists(path_save+file)):
                                        values = tmp
                                       
                                    
                                    if(count > 0):
                                        for v,t in zip(values, tmp):
                                            if v != 'Value' and t != 'Value':
                                                #se annotazione valida
                                                dif = float(v)/count - float(t)
                                                valueDiffExpert += dif                                                 
                                    else:
                                        valuesTmp = values
                                         
                        frames = csv_list[0]
                        timestamps = csv_list[1]

                        valueDiffExpert = valueDiffExpert/len(frames)
                        dictExpertCoeff.update({annotator:valueDiffExpert})
                
                    else:

                        if(count == 0): 
                            frames = []
                            timestamps = []
     
    #print(dictExpertCoeff)               
    return dim, frames, timestamps, dictExpertCoeff     
                                   
def writeValuesCSV(videoName, dim, csv_list, value):   
    path = path_save + 'expert_valence_' + videoName + '.csv' if value=='valence' else path_save + 'expert_arousal_' + videoName + '.csv'
    with open(path, 'w') as outfile:
        
        for i in range(0, dim-1):
            k=0
            for entries in csv_list:
                if k!=0:
                    outfile.write(';')  
                   
                outfile.write(str(entries[i]))
               
                k+=1
            outfile.write('\n')
             
                                
def main():

    videos = list()
    
    #check sui video della cartella videos per sapere il nome dei video da elaborare
    for video in os.listdir(path_videos):

        valence = list()
        arousal = list()
        csv_listV = list()
        csv_listA = list()

        if os.path.join(path_videos, video) != os.path.join(path_videos, 'Example.mp4'):
        
            #estraggo solo il file name senza estensione
            base = (basename(video))
            videoName = os.path.splitext(base)[0]
            
            print("\n\nElabrating video: " + videoName)
           
            #calcolo valence di ogni video
            print('....is writing valence')
            dim, frame, timestamp, dictExpertCoeff = getExpertValues(videoName, 'valence')
            
            valence = calculateEWE(dictExpertCoeff, video,dim, "valence")
        
            if dim !=0 and frame != [] and timestamp != [] and valence != []:
                csv_listV.append(frame)
                csv_listV.append(timestamp)
                csv_listV.append(valence)
                writeValuesCSV(videoName, dim, csv_listV, 'valence')
               
            else:
                print('no values')
            
            
            #calcolo l'arousal di ogni video
            print('.....is writing arousal')
            dim, frame, timestamp, dictExpertCoeff = getExpertValues(videoName, 'arousal')
            valence = calculateEWE(dictExpertCoeff, video, dim,  "arousal")
            if dim !=0 and frame != [] and timestamp != [] and arousal != []:
                csv_listA.append(frame)
                csv_listA.append(timestamp)
                csv_listA.append(arousal)
                writeValuesCSV(videoName, dim, csv_listA, 'arousal')
            else:
                print('no values')
                
#richamo il main
main()
