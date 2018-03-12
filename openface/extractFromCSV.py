import csv
import os
import glob

path_store = 'D:/Projects/DANTE/openface/*.csv'
path_save = 'D:/Projects/DANTE/openface/csv/'

def readFromCSV(spamReader):

    frame = list()
    timestamp = list()
    left_landmark = list()
    right_landmark = list()
    top_landmark = list()
    bottom_landmark = list()

    csv_list = list()

    #leggi csv e crea struttura dati per salvare i valori
    for row in spamReader:
        #num of frame
        frame.append(row[0])
        #timestamp
        timestamp.append(row[1])
        #landmark_x 0 
        left_landmark.append(row[298])
        #landmark_x 16 
        right_landmark.append(row[314])
        #landmark_y 21
        top_landmark.append(row[387])
        #landmark_y 8
        bottom_landmark.append(row[374])
    
    #crea una struttura dati che contenga tutti gli elementi che andranno messi nel csv
    csv_list.append(frame)
    csv_list.append(timestamp)
    csv_list.append(left_landmark)
    csv_list.append(right_landmark)
    csv_list.append(top_landmark)
    csv_list.append(bottom_landmark)

    return len(frame), csv_list

def writeIntoCSV(file_name, dim, csv_list):
    #scrivi nuovo csv
    with open(path_save + 'reduced_' + file_name, 'w') as outfile:

        #ciclo su tutti i frame
        for i in range(0, dim):
            #controllo sul primo valore pre non mettere il carattere ','
            k=0
            #ciclo sugli array all'interno di csv_list (ovvero tutti i valori che mi servono)
            for entries in csv_list:
                if k!=0:
                    outfile.write(',')  
                outfile.write(entries[i])
                k+=1
            outfile.write('\n')

def alreadyExists(file_name):
    for xpath in glob.glob(path_save + 'reduced_' + file_name): 
        tmp = 'reduced_'+ file_name
        if tmp == os.path.basename(xpath):
            return False
    return True
           
                
            
def main():

    #glob.glob(path_store) è un metodo di blob che rutorna tutti i path dei file in path_store
    for path_name in glob.glob(path_store):

        #tiro fuori il nome del file senza il path
        file_name = os.path.basename(path_name)

        if alreadyExists(file_name): 
        
            print(os.path.basename(file_name) + ' opened')
            #creo l' oggetto reader per lettura da file .csv
            spamReader = csv.reader(open(path_name, newline=''))

            #leggo
            dim, csv_list = readFromCSV(spamReader)

            #scrivo
            writeIntoCSV(file_name, dim, csv_list)

            print(os.path.basename('reduce file completed, total frame: ' + str(dim) + '\n'))
        
        else:
            print('\n' + os.path.basename(file_name) + ' already restricted, delete the reduced file to recalculate it')
                
            
                
            
main()




        


    

