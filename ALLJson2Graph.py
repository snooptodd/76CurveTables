## create graphs for the live and pts json files 

# get list of files in live/json, live/jsonalt, pts/json, pts/jsonalt
# loop through each list creating a graph including the matches from the other lists
# super inefficent but pyplot hopefully dosent overwrite by default. 

###### make some test files in the json folders 
# probalem for future me

import os
import subprocess
import shutil
import pathlib
import filecmp
import json
import matplotlib.pyplot as plt

DEBUG=False
RootDir="./json"
#livePatch="/PTS_10OCT24"
LIVEDIR="/Live_P58"
PTSDIR="/PTS_P60_11apr"
CommonDIR='/misc/curvetables'
SearchName="*.json"
PTSDIRList=[]
LIVEDIRList=[]

if DEBUG :
    LIVEDIR="/test_live"
    PTSDIR="/test_pts"

# Specify the directory path you want to start from

# PTSDIRList=list_files_recursive(RootDir+PTSDIR)
# LIVEDIRList=list_files_recursive(RootDir+LIVEDIR+CommonDIR)

def makegraph():
    file1X=[]
    file1Y=[]
    file2X=[]
    file2Y=[]
    file3X=[]
    file3Y=[]
    file4X=[]
    file4Y=[]
    # file1=PTSfile
    # file2=LiveFile

    if DEBUG :
        print("DEBUG\n%s\n%s\n%s\n%s\n" % (file1, file2, file3, file4))
        return
    
    # Load JSON data from a file and extract the x and y data
    
    if file1 != '':
        title=file1.stem
        searchpath = RootDir+PTSDIR+CommonDIR+'/jsonalt/'
        pathtmp = str(file1.parent)[str(file1.parent).find('/jsonalt')+8:]   
        with open(file1, 'r') as file:
            file1_json_data = json.load(file)
            file.close
        for entry in file1_json_data["curve"]:
            # print(entry)
            file1X.append(entry["x"])
            file1Y.append(entry["y"])
        plt.plot(file1X,file1Y, label=str(PTSDIR)[1:]+' jsonAlt'+pathtmp, marker = 'o', markevery=0.1 )
        for key,value in enumerate(file1X):
            if not value%10:
                plt.annotate('(' + str(file1X[key]) + ', ' + str(file1Y[key]) + ')',(file1X[key], file1Y[key]))

    if file2 != '':
        title=(file2.stem)
        pathtmp = str(file2.parent)[str(file2.parent).find('/json',10)+5:]
        with open(file2, 'r') as file:
            file2_json_data = json.load(file)
            file.close
        for entry in file2_json_data["curve"]:
            # print(entry)
            file2X.append(entry["x"])
            file2Y.append(entry["y"])
        plt.plot(file2X,file2Y, label=str(PTSDIR)[1:]+" json"+pathtmp, marker = '*', markevery=0.1)
        for key,value in enumerate(file2X):
            if not value%10:
                plt.annotate('(' + str(file2X[key]) + ', ' + str(file2Y[key]) + ')',(file2X[key], file2Y[key]))

    if file3 != '':
        title=(file3.stem)
        pathtmp = str(file3.parent)[str(file3.parent).find('/jsonalt')+8:]       
        with open(file3, 'r') as file:
            file3_json_data = json.load(file)
            file.close
        for entry in file3_json_data["curve"]:
            # print(entry)
            file3X.append(entry["x"])
            file3Y.append(entry["y"])
        plt.plot(file3X,file3Y, label=str(LIVEDIR)[1:]+" jsonAlt"+pathtmp, marker = 'x', markevery=0.1)
        for key,value in enumerate(file3X):
            if not value%10:
                plt.annotate('(' + str(file3X[key]) + ', ' + str(file3Y[key]) + ')',(file3X[key], file3Y[key]))

    if file4 != '':
        title=(file4.stem)
        pathtmp = str(file4.parent)[str(file4.parent).find('/json',10)+5:]
        with open(file4, 'r') as file:
            file4_json_data = json.load(file)
            file.close
        for entry in file4_json_data["curve"]:
            # print(entry)
            file4X.append(entry["x"])
            file4Y.append(entry["y"]) 
        plt.plot(file4X,file4Y, label=str(LIVEDIR)[1:]+" json"+pathtmp, marker = '+', markevery=0.1)   
        for key,value in enumerate(file4X):
            if not value%10:
                plt.annotate('(' + str(file4X[key]) + ', ' + str(file4Y[key]) + ')',(file4X[key], file4Y[key]))

    # Plotting
    xlabel="X"
    ylabel="Y"
    savePath="./graphs"+pathtmp+"/" #return path from past jsonalt. done above
    saveName=title+'.png'
    # check if path exist and if not create it.
    if not os.path.isdir(savePath):
        os.makedirs(savePath)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel,rotation=0)
    plt.title(title)
    plt.legend()
    plt.savefig(savePath+saveName)
    plt.close()

    return 


# # get list of json files in dirs

PTSJsonaltPath = pathlib.Path(RootDir+PTSDIR+CommonDIR+"/jsonalt")
PTSJsonPath = pathlib.Path(RootDir+PTSDIR+CommonDIR+"/json")
# PTSJsonaltDIRList = list(PTSJsonaltPath.rglob(SearchName))
PTSPath = pathlib.Path(RootDir+PTSDIR+CommonDIR)
PTSDIRList = list(PTSPath.rglob(SearchName))
LiveJsonaltPath = pathlib.Path(RootDir+LIVEDIR+CommonDIR+"/jsonalt")
LiveJsonPath = pathlib.Path(RootDir+LIVEDIR+CommonDIR+"/json")
# LiveJsonaltDIRList = list(LiveJsonaltPath.rglob(SearchName))
LivePath = pathlib.Path(RootDir+LIVEDIR+CommonDIR)
LiveDIRList = list(LivePath.rglob(SearchName))
file=""
all=set(())
# loop through PTSDIRList. sets do not allow duplicates. each fiile will only be listed one time.
# 
for file in PTSDIRList:
    all.add(file.name)
for file in LiveDIRList:
    all.add(file.name)

print(len(all))

for name in all:
    file1 = file2 = file3 = file4 = file = ''
    for file in PTSJsonaltPath.rglob(name):
        file1 = file
    file = ''
    for file in PTSJsonPath.rglob(name):
        file2 = file
    file = ''
    for file in LiveJsonaltPath.rglob(name):
        file3 = file
    file = ''
    for file in LiveJsonPath.rglob(name):
        file4 = file
    file = ''

    makegraph()