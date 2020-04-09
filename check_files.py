#Creates empty text files for plastic spotter project when no plastic is in the picture with would result in no text file being generated
#work for subfolders

import os

def make_text_files(full_path):
    pictures = []
    text = []
    null_file = []

    #Pictures
    path = full_path + "images"
    for r, d, f in os.walk(path):
        for file in f:
            pictures.append(file.replace('.JPG',''))
    #end

    #Text files
    path = full_path + "labels"
    for r, d, f in os.walk(path):
        for file in f:
            text.append(file.replace('.txt',''))
    #end

    for picture in pictures:
        if picture not in text:
            null_file.append(picture + '.txt')

    #Create Empty Text file
    path = full_path + "labels\\"
    for file in null_file:
        #Create empty text file
        print(file)
        f= open(path + file,"w+")
        f.close()
    #end
#end