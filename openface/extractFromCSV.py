import csv

frame = list()
timestamp = list()
left_landmark = list()
right_landmark = list()
top_landmark = list()
bottom_landmark = list()

csv_list = list()

def readFromCSV(spamReader):
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

def writeIntoCSV(file_name):
    #scrivi nuovo csv
    with open(file_name + '_small.csv', 'w') as outfile:
        dim = len(frame)
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

def main():
    #specifica il filename del tuo csv che vuoi rimpiccolire
    file_name = input('Inserisci il nome del file: ')

    #creo l' oggetto reader per lettura da file .csv
    spamReader = csv.reader(open(file_name + '.csv', newline=''))

    #leggo
    readFromCSV(spamReader)

    #scrivo
    writeIntoCSV(file_name)

main()




        


    

