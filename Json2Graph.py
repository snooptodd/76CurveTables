## compare the live and pts json files for Differences and if Different plot them (maybe put the data in the plot too)
# for Live we need to search both json paths 
#  i suppose to start we get a list of all files in the ptsdir jsonalt dir 
#  then search the livedir for the same json files and compare (cmp) them ( we might(probably) need to prioritize jsonalt dir )
#  create a graph if they are Different.
#  convert the json data to somthing gnuplot can understand (jq -r '.curve[]| join(" ")')
#  save the plot to svg or something.

###### make some test files in the json folders
	# OK # test if live jsonalt is same as PTS jsonalt nothing is printed
	# OK # test if both Live json are different only jsonalt is printed
	# OK # test if live jsonalt dosent exist and the live json is differnt print 
	# OK # test if live jsonalt dosent exist and the live json is same no print 

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
LIVEDIR="/PTS_25OCT24"
PTSDIR="/PTS_01NOV24"
CommonDIR='/misc/curvetables'
SearchName="*"
JsonaltOnly=False
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
    file1=PTSfile
    file2=LiveFile

    if DEBUG :
        print("DEBUG\n%s\n%s\n" % (file1, file2))
        return
    
    # Load JSON data from a file and extract the x and y data
    with open(file1, 'r') as file:
        file1_json_data = json.load(file)
    for entry in file1_json_data["curve"]:
        # print(entry)
        file1X.append(entry["x"])
        file1Y.append(entry["y"])
    if file2.find(".json") < 0:
        ...
    else:
        with open(file2, 'r') as file:
            file2_json_data = json.load(file)
        for entry in file2_json_data["curve"]:
            # print(entry)
            file2X.append(entry["x"])
            file2Y.append(entry["y"])    
    
    # Plotting
    xlabel="X"
    ylabel="Y"
    title=str(file1.stem)
    pathtmp=str(file1.parent)
    savePath="./graphs"+pathtmp[pathtmp.find("jsonalt")+7:]+"/" #return path from past jsonalt.
    saveName=title+'.png'
    # check if path exist and if not create it.
    if not os.path.isdir(savePath):
        os.makedirs(savePath)
        
    plt.plot(file1X,file1Y, label=str(PTSDIR)[1:])
    if file2.find(".json") > 0:
        plt.plot(file2X,file2Y, label=str(LIVEDIR)[1:])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    for key,value in enumerate(file1X):
        if not value%10:
            plt.annotate('(' + str(file1X[key]) + ', ' + str(file1Y[key]) + ')',(file1X[key], file1Y[key]))
    plt.savefig(savePath+saveName)
    plt.close()

    return 


# # get list of json files in dirs

PTStemp = pathlib.Path(RootDir+PTSDIR+CommonDIR+"/jsonalt")
PTSDIRList=PTStemp.rglob(SearchName)
# loop through PTSDIRList
for PTSfile in PTSDIRList: 
# 	# get list of files in livedir that match PTSFile
#### FIX THIS 
# probably nuke it and add logic below to handle Jsonaltonly
    # if JsonaltOnly:
    # # only look in jsonalt path
    #     LIVEtemp = pathlib.Path(RootDir+LIVEDIR+CommonDIR+"/jsonalt/")
    # else:
    #     LIVEtemp = pathlib.Path(RootDir+LIVEDIR+CommonDIR+"/")

    # LIVEDIRList=list(LIVEtemp.rglob(PTSfile.name))
    PTStmp=str(PTSfile.parent)+"/"
    liveALTtmp=PTStmp.replace(PTSDIR,LIVEDIR)
    liveJSONtmp=liveALTtmp.replace('jsonalt','json')
    ALT_match, ALT_mismatch, ALT_errors=filecmp.cmpfiles(PTStmp,liveALTtmp,[str(PTSfile.name)],shallow=False)
    JSON_match, JSON_mismatch, JSON_errors=filecmp.cmpfiles(PTStmp,liveJSONtmp,[str(PTSfile.name)],shallow=False)
    # _errors = means a file was found in the pts dir but not the search dir.
    # _mismatch means that the files do not match
    # _match means they do match

    ## Add JsonAltOnly logic 
    if JsonaltOnly :
        # we dont want to make a graph if a file exists in the json folder because we are only interested in new or changed files in the jsonalt folder.
        # if pts jsonalt dose not exist anywhre else make graph
        # if pts jsonalt is different than live jsonalt make graph
        # if pts jsonalt is (i think that is it)
        
        if len(ALT_errors):
            if len(JSON_match) or len(JSON_mismatch):
                continue
            LiveFile=""
            makegraph()
        elif len(ALT_mismatch):
            LiveFile=liveALTtmp+str(PTSfile.name)
            makegraph()
        continue



    # if both match do not print
    if len(ALT_match) and len(JSON_match) :
        continue

    # If both mismatch print alt PTSfile vs live jsonalt
    # if ALT_mismatch and JSON_errors print PTSFILE vs live jsonalt
    # if ALT_mismatch and JSON_match print PTSFILE vs live jsonalt
    if len(ALT_mismatch):
        if len(JSON_mismatch) or len(JSON_match) or len(JSON_errors): # this does nothing
            LiveFile=liveALTtmp+str(PTSfile.name)
            makegraph()
            continue
    
    # if both errors print PTSfile vs nothing
    # if ALT_errors and JSON_mismatch print PTSFILE vs live json
    if len(ALT_errors) :
        if len(JSON_errors):
            LiveFile =""
            makegraph()
            continue
        elif len(JSON_mismatch) :
            LiveFile=liveJSONtmp+str(PTSfile.name)
            makegraph()
            continue
    
    # if ALT_match and JSON_mismatch print PTSFILE vs live json
    if len(ALT_match) and len(JSON_mismatch):
        LiveFile=liveJSONtmp+str(PTSfile.name)
        makegraph()
        continue
        
# # 	# if LIVEDIRList is has more than 2 entries we will have probalems lets check for it and hope it never happens. 
#     if len(LIVEDIRList) > 2:
#         print("more than 2 files matched quitting. %s" , PTSfile.name)
#         exit

#     Jsonalt=False
# # 	# LIVEDIRList only has the files that match the file we are looking for. so if jsonalt is found in the string then we only plot the jsonalt file. 
#     if any(["jsonalt" in element.parts for element in LIVEDIRList]):
#         Jsonalt=True

#     for LiveFile in LIVEDIRList:
#         if filecmp.cmp(LiveFile,PTSfile, shallow=False):
#             continue

# # 		# We only want to create 1 graph from the files that match $iPTS and we want to prioritize the jsonalt folder
# # 		# so we need to check if LiveFile currently contains jsonalt
# # 		# and if jsonalt was found at all in the list 
#         if ("jsonalt" in LiveFile.parts) and Jsonalt:
#             makegraph()
#         elif not Jsonalt:
#             makegraph()
