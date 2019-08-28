import os

file = open('images_list.txt','r')

lines = file.readlines()
edited_lines = []

#Remove paths from names
for line in lines:
    edited_lines.append(line.replace('/home/n9960392/darknet/data/training_set_1/images/test/','').replace('.JPG\n',''))
#end

file = open('lsit2.txt','r')

lines = file.readlines()
edited_files = []

#Remove paths from names
for line in lines:
    edited_files.append(line.replace('/home/n9960392/darknet/data/training_set_1/labels/test/','').replace('.txt\n',''))
#end


#Create empty text files if THEY DO NOT ALREADY EXIST
for obj in edited_lines:
    if obj not in edited_files:
        open('test\\'+ obj + '.txt','w+')
    #end
#end