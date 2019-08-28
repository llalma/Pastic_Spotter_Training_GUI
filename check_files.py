#Creates empty text files for plastic spotter project when no plastic is in the picture with would result in no text file being generated

import os

pictures = []
text = []
null_file = []

#Pictures
path = "C:\\Users\\Liam Hulsman-Benson\\Google Drive\\Plastic_Spotter\\data\\Aspect_UAV_MarineLitter_project\\20190813\\images"
for r, d, f in os.walk(path):
    for file in f:
        pictures.append(file.replace('.JPG',''))
#end

#Text files
path = "C:\\Users\\Liam Hulsman-Benson\\Google Drive\\Plastic_Spotter\\data\\Aspect_UAV_MarineLitter_project\\20190813\\labels"
for r, d, f in os.walk(path):
    for file in f:
        text.append(file.replace('.txt',''))
#end

for picture in pictures:
    if picture not in text:
        null_file.append(picture + '.txt')

#Create Empty Text file
path = path = "C:\\Users\\Liam Hulsman-Benson\\Google Drive\\Plastic_Spotter\\data\\Aspect_UAV_MarineLitter_project\\20190813\\labels\\"
for file in null_file:
    #Create empty text file
    print(file)
    f= open(path + file,"w+")
    f.close()
#end