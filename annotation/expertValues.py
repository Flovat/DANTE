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


def readValenceFromCSV(spamReader):
    frameV = list()
    timestampV = list()
    valueV = list()
    csv_listV = list()

    count = -1
    
    for row in spamReader:
        if (count==-1):
            frameV.append('Frame')
        else:
            frameV.append(count)   
        timestampV.append(row[0])
        valueV.append(row[4])
        count+=1

    csv_listV.append(frameV)
    csv_listV.append(timestampV)
    csv_listV.append(valueV)
    
    return len(frameV), csv_listV

def readArousalFromCSV(spamReader):
    frameA = list()
    timestampA = list()
    valueA = list()
    csv_listA = list()

    count = -1
    
    for row in spamReader:
        if (count==-1):
            frameA.append('Frame')
        else:
            frameA.append(count)    
        timestampA.append(row[0])
        valueA.append(row[4])
        count+=1

    csv_listA.append(frameA)
    csv_listA.append(timestampA)
    csv_listA.append(valueA)
    
    return len(frameA), csv_listA
        

def getExpertValence(video):
    valence = list()
    valenceTmp = list()
    valenceAvg = list()
    dim = 0
    count = 0

    for annotator in os.listdir(path_store):
        if os.path.isdir(os.path.join(path_store, annotator)) and annotator!='expert':
            #print(annotator)
            
            for vid in os.listdir(path_store+annotator):

                if vid == video + '_mp4':
                    #print(vid)

                    path_name = path_store+annotator+'/'+vid+'/'+'valence.csv'
                    if os.path.exists(path_name):
                        count+=1
                        #open file and extract values
                        with open(path_name, 'rt') as csvfile:
                                    spamReader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                    dim, csv_list = readValenceFromCSV(spamReader)
                                    tmp = csv_list[2]
                                    #print(tmp)
                                    if not valence:
                                        valence = tmp
                                    else:
                                        
                                        for f,b in zip(valence, tmp):
                                            if f!= 'Value' and b!= 'Value':
                                                valenceTmp.append(float(f)+float(b))
                        for i in valenceTmp:
                            valence.append(i/count)   
  
                        frames = csv_list[0]
                        timestamps = csv_list[1]
                              

                    else:
                        print('valori non esistenti per annotatore: ' + annotator)
                        if(count == 0): 
                            frames = []
                            timestamps = []
                            
                        
    return dim, frames, timestamps, valence     
   

    


def getExpertArousal(video):
    arousal = list()
    arousalTmp = list()
    arousalAvg = list()
    dim = 0
    count = 0

    for annotator in os.listdir(path_store):
       
        if os.path.isdir(os.path.join(path_store, annotator)) and annotator!='expert':
            #print(annotator)
            
            for vid in os.listdir(path_store+annotator):

                if vid == video + '_mp4':
                    #print(vid)

                    path_name = path_store+annotator+'/'+vid+'/'+'arousal.csv'

       
                    if os.path.exists(path_name):
                        count+=1
                        #open file and extract values
                        with open(path_name, 'rt') as csvfile:
                                    spamReader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                    dim, csv_listA = readArousalFromCSV(spamReader)
                                    tmp = csv_listA[2]
                                    #print(tmp)
                                    if not arousal:
                                        arousal = tmp
                                    else:
                                        
                                        for f,b in zip(arousal, tmp):
                                            if f!= 'Value' and b!= 'Value':
                                                arousalTmp.append(float(f)+float(b))
                        
                        for i in arousalTmp:
                            arousal.append(i/count)
                        
                        frames = csv_listA[0]
                        timestamps = csv_listA[1]
                              

                    else:
                        print('valori non esistenti per annotatore: ' + annotator)
                        if(count == 0): 
                            frames = []
                            timestamps = []
                            
                        
    return dim, frames, timestamps, arousal     
                         
                                   
                                    
                                    

def writeValenceCSV(videoName, dim, csv_list):   
    with open(path_save + 'expert_valence_' + videoName + '.csv', 'w') as outfile:
        
        for i in range(0, dim-1):
            k=0
            for entries in csv_list:
                if k!=0:
                    outfile.write(';')  
                   
                outfile.write(str(entries[i]))
                k+=1
            outfile.write('\n')

def writeArousalCSV(videoName, dim, csv_list):   
    with open(path_save + 'expert_arousal_' + videoName + '.csv', 'w') as outfile:
        
        for i in range(0, dim-2):
            k=0
            for entries in csv_list:
                if k!=0:
                    outfile.write(';')  
                   
                outfile.write(str(entries[i]))
                k+=1
            outfile.write('\n')




def alreadyExists(file_name):
    #print(file_name)
    for xpath in glob.glob(path_save): 
        tmp = file_name
        
        if tmp == os.path.basename(xpath):
            return False
    return True               
                                

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

            dimV, frameV, timestampV, valence = getExpertValence(videoName)
            if dimV !=0 and frameV != [] and timestampV != [] and valence != []:
                csv_listV.append(frameV)
                csv_listV.append(timestampV)
                csv_listV.append(valence)
                writeValenceCSV(videoName, dimV, csv_listV)
            else:
                print('non scrivo i valori')
            
            
            
            print('.....is writing arousal')
            dimA, frameA, timestampA, arousal = getExpertArousal(videoName)
            if dimA !=0 and frameA != [] and timestampA != [] and arousal != []:
                csv_listA.append(frameA)
                csv_listA.append(timestampA)
                csv_listA.append(arousal)
                writeArousalCSV(videoName, dimA, csv_listA)
            else:
                print('non scrivo i valori')
                
           
            



main()
