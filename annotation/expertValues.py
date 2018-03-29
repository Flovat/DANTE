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

def getExpertValues(video, value):
    values = list()
    valuesTmp = list()
    valuesAvg = list()
    dim = 0
    count = 0
    frames = list()
    timestamps = list()

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
                        print('\nvalori esistenti per annotatore: ' + annotator)
                        count += 1
                        
                        #open file and extract values
                        with open(path_name, 'rt') as csvfile:
                                    spamReader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                    dim, csv_list = readValuesFromCSV(spamReader)
                                    tmp = csv_list[2]
                            


                                    #EWE
                                    #for ogni valore controlla che:
                                        #if la media aritmetica fino a ora è vicino al nuovo valore allora somma anche loro
                                        #else scarta il valore e non incrementare il count perchè troppo distante quindi incline a errore

                                    #prendi i valori dell'esperto se esiste un esperto per usarlo come primo termine di paragone........
                                                                      
                                    if (not os.path.exists(path_save+file)):
                                        values = tmp
                                       
                                            
                                    if(count > 1):
                                        for v,t in zip(values, tmp):
                                            if v != 'Value' and t != 'Value':

                                                
                                                #se annotazione valida
                                                dif = float(v)/count - float(t)
                                                if (dif < 0.3 and dif > -0.3):
                                                    #print('True' + str(dif))

                                                    #print('v: '+v)
                                                    
                                                    valuesTmp.append((float(v) + float(t))/count)
                                                    
                                                    #print(str(float(v) + float(t)))
                                                else:
                                                    valuesTmp.append(v)
                                                    #print('False', str(dif))
                                                        
                                    else:
                                        valuesTmp = values
                                         
                                        
                                    
                                   
                        values = list()
                        #.........e poi dividendoli per il numero di annotatori di quel video
                        #print('\n\n'+str(count) + ' ' + 'temp   ' + str(valuesTmp))
                        for i in valuesTmp:
                           
                            if i=='Value':
                               
                                values.append('Value')
                            else:
                                
                                values.append((float(i)) )
                        
                        frames = csv_list[0]
                        timestamps = csv_list[1]

                              

                    else:
                        #print('valori non esistenti per annotatore: ' + annotator)
                        if(count == 0): 
                            frames = []
                            timestamps = []
    #print('values' + str(values))                     
    return dim, frames, timestamps, values     
                                   
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
            
            print("Elabrating video: " + videoName)
           
            #calcolo valence di ogni video
            print('....is writing valence')
            dim, frame, timestamp, valence = getExpertValues(videoName, 'valence')
            if dim !=0 and frame != [] and timestamp != [] and valence != []:
                csv_listV.append(frame)
                csv_listV.append(timestamp)
                csv_listV.append(valence)
                writeValuesCSV(videoName, dim, csv_listV, 'valence')
            else:
                print('no values')
            
            
            #calcolo l'arousal di ogni video
            print('.....is writing arousal')
            dim, frame, timestamp, arousal = getExpertValues(videoName, 'arousal')
            if dim !=0 and frame != [] and timestamp != [] and arousal != []:
                csv_listA.append(frame)
                csv_listA.append(timestamp)
                csv_listA.append(arousal)
                writeValuesCSV(videoName, dim, csv_listA, 'arousal')
            else:
                print('no values')
                
#richamo il main
main()