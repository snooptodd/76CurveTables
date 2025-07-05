#!/bin/python3

# ## create graphs and pages for the live and pts json files 

# get list of files in live, pts
# loop through list creating a graph and page including the matching json file from the live/pts,json/jsonalt dirs
# super inefficent but it works.

###### make some test files in the json folders 
# they are there "just" need to write up the test

import os
import pathlib
import json
import filecmp
import matplotlib.pyplot as plt

DEBUG=False
ROOT_DIR="./json"
LIVE_DIR="/Live_P60"
PTS_DIR="/PTS_P62_3July"
COMMON_DIR='/misc/curvetables'
SEARCH_NAME="*.json"
PTSDIRList=[]
LIVEDIRList=[]
PTSJsonaltPath = PTSJsonPath = PTSPath = PTSDIRList = LiveJsonaltPath = LiveJsonPath = LivePath = LiveDIRList = file = file1 = file2 = file3 = file4 = indexhtml = ""
all=set(())

if DEBUG :
    LIVE_DIR="/test_live"
    PTS_DIR="/test_pts"


def htmlheader(pagename):
    return f'''<!DOCTYPE html> <html lang="en"> 
<head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> 	
<title>{pagename}</title> 
<script src="sortable.min.js"></script>
<link rel="stylesheet" href="sortable-theme-minimal.css" />
<link rel="stylesheet" href="/76CurveTables/styles.css"> </head> <body>'''

def htmlfooter():
    return '</body> </html>'

def tablestart(col1,col2,col3,col4):
    return f'''<table data-sortable>
      <caption></caption>
      <thead>
        <th>{col1}</th>
        <th>{col2}</th>
        <th>{col3}</th>
        <th>{col4}</th>
      </thead>
      <tbody>
    '''

def tablerow(col1,col2,col3,col4):
    return f'''  <tr><td>{col1}</td><td>{col2}</td><td>{col3}</td><td>{col4}</td></tr>'''

def tableend():
    return '</tbody></table>'

def writefile(nameandpath, data):
    f = open(nameandpath, "w")
    f.write(data)
    f.close()

def makegraph():
    file1X=[]
    file1Y=[]
    file2X=[]
    file2Y=[]
    file3X=[]
    file3Y=[]
    file4X=[]
    file4Y=[]
    title = pathtmp = subpagehtml = ''
    file1subpagehtml = file2subpagehtml = file3subpagehtml = file4subpagehtml = ''
    file1txtdata = file2txtdata = file3txtdata = file4txtdata = ''
    global indexhtml

    if DEBUG :
        print("DEBUG\n%s\n%s\n%s\n%s\n" % (file1, file2, file3, file4))
        return
    
    # Load JSON data from a file and extract the x and y data
        
    if file1 != '':
        title=file1.stem
        pathtmp = str(file1.parent)[str(file1.parent).find('/jsonalt')+8:]
        with open(file1, 'r') as file:
            file1_json_data = json.load(file)
            file.close
        for entry in file1_json_data["curve"]:
            # print(entry)
            file1txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file1X.append(entry["x"])
            file1Y.append(entry["y"])
        plt.plot(file1X,file1Y, label=str(PTS_DIR)[1:]+' jsonAlt', marker = 'o', markevery=0.1 )
        for key,value in enumerate(file1X):
            if not value%10:
                plt.annotate('(' + str(file1X[key]) + ', ' + str(file1Y[key]) + ')',(file1X[key], file1Y[key]))
        file1subpagehtml+=f'<label for="ptsjsonalt">{file1}</label> <div class="box" id="ptsjsonalt">{file1txtdata}</div>'

    if file2 != '':
        title=(file2.stem)
        pathtmp = str(file2.parent)[str(file2.parent).find('/json',10)+5:]
        with open(file2, 'r') as file:
            file2_json_data = json.load(file)
            file.close
        for entry in file2_json_data["curve"]:
            # print(entry)
            file2txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file2X.append(entry["x"])
            file2Y.append(entry["y"])
        plt.plot(file2X,file2Y, label=str(PTS_DIR)[1:]+" json", marker = '*', markevery=0.1)
        for key,value in enumerate(file2X):
            if not value%10:
                plt.annotate('(' + str(file2X[key]) + ', ' + str(file2Y[key]) + ')',(file2X[key], file2Y[key]))
        file2subpagehtml+=f'<label for="ptsjson">{file2}</label> <div class="box" id="ptsjson">{file2txtdata}</div>'

    if file3 != '':
        title=(file3.stem)
        pathtmp = str(file3.parent)[str(file3.parent).find('/jsonalt')+8:]       
        with open(file3, 'r') as file:
            file3_json_data = json.load(file)
            file.close
        for entry in file3_json_data["curve"]:
            # print(entry)
            file3txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file3X.append(entry["x"])
            file3Y.append(entry["y"])
        plt.plot(file3X,file3Y, label=str(LIVE_DIR)[1:]+" jsonAlt", marker = 'x', markevery=0.1)
        for key,value in enumerate(file3X):
            if not value%10:
                plt.annotate('(' + str(file3X[key]) + ', ' + str(file3Y[key]) + ')',(file3X[key], file3Y[key]))
        file3subpagehtml+=f'<label for="Livejsonalt">{file3}</label> <div class="box" id="Livejsonalt">{file3txtdata}</div>'

    if file4 != '':
        title=(file4.stem)
        pathtmp = str(file4.parent)[str(file4.parent).find('/json',10)+5:]
        with open(file4, 'r') as file:
            file4_json_data = json.load(file)
            file.close
        for entry in file4_json_data["curve"]:
            # print(entry)
            file4txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file4X.append(entry["x"])
            file4Y.append(entry["y"]) 
        plt.plot(file4X,file4Y, label=str(LIVE_DIR)[1:]+" json", marker = '+', markevery=0.1)   
        for key,value in enumerate(file4X):
            if not value%10:
                plt.annotate('(' + str(file4X[key]) + ', ' + str(file4Y[key]) + ')',(file4X[key], file4Y[key]))
        file4subpagehtml+=f'<label for="Livejson">{file4}</label> <div class="box" id="Livejson">{file4txtdata}</div>'

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
    subpagehtml+=f'''{htmlheader(title)}
<img src="{saveName}"><p>
<table><tr><td>{file1subpagehtml}</td><td>{file2subpagehtml}</td></tr>
<tr><td>{file3subpagehtml}</td><td>{file4subpagehtml}</td></tr></table>
{htmlfooter()}'''
    writefile(savePath+title+'.html', subpagehtml)
    # indexhtml+=f'<a href="{savePath+title+'.html'}">{title}</a><p>'
    indexhtml+=tablerow(f'<a href="{savePath+title+'.html'}">{title}</a>',ptsnew,ptsmissing,ptschanged)
    return 


# # get list of json files in dirs

PTSJsonaltPath = pathlib.Path(ROOT_DIR+PTS_DIR+COMMON_DIR+"/jsonalt")
PTSJsonPath = pathlib.Path(ROOT_DIR+PTS_DIR+COMMON_DIR+"/json")
PTSPath = pathlib.Path(ROOT_DIR+PTS_DIR+COMMON_DIR)
PTSDIRList = list(PTSPath.rglob(SEARCH_NAME))
LiveJsonaltPath = pathlib.Path(ROOT_DIR+LIVE_DIR+COMMON_DIR+"/jsonalt")
LiveJsonPath = pathlib.Path(ROOT_DIR+LIVE_DIR+COMMON_DIR+"/json")
LivePath = pathlib.Path(ROOT_DIR+LIVE_DIR+COMMON_DIR)
LiveDIRList = list(LivePath.rglob(SEARCH_NAME))

# check that we found something in both dir paths.
if len(PTSDIRList) == 0:
    exit('PTS dir empty')

if len(LiveDIRList) == 0:
    exit('Live dir empty')
    

# loop through PTSDIRList. sets do not allow duplicates. each fiile will only be listed one time.
# 
for file in PTSDIRList:
    all.add(file.name)
for file in LiveDIRList:
    all.add(file.name)
alllist = list(all)
alllist.sort()
print(len(all))
indexhtml=htmlheader('Curve Table Graphs')
indexhtml+=tablestart('Name','PTS New','PTS Missing','PTS Changed')

for name in alllist:
    # want to show on the page if a flle is changed new or removed in the pts
    # 
    # i alredy have the different files looked up and will use them to test for changes.

    # PTS New is file found in PTS and not in Live
    ## if file3 and file4 not found then PTS New

    # PTS missing is file found in Live and not in PTS
    ## if file1 and file2 not found then PTS missing

    # PTS changed is file found in both and the file is changed.
    ## if file1 and file3 are found and different then PTS changed.
    ## or if file2 and file4 are found and differnet then PTS changed.

    file1 = file2 = file3 = file4 = file = ''
    ptsnew = ptsmissing = ptschanged = ''
    for file in PTSJsonaltPath.rglob(name):
        file1 = file
    for file in PTSJsonPath.rglob(name):
        file2 = file
    for file in LiveJsonaltPath.rglob(name):
        file3 = file
    for file in LiveJsonPath.rglob(name):
        file4 = file

    if file3=='' and file4=='':
        ptsnew=True

    if file1=='' and file2=='':
        ptsmissing=True

    if file1!='' and file3!='':
        if not filecmp.cmp(file1,file3,shallow=False):
            ptschanged=True

    if file2!='' and file4!='':
        if not filecmp.cmp(file2,file4,shallow=False):
            ptschanged=True
    makegraph()

indexhtml+=tableend()
indexhtml+=htmlfooter()
writefile('./index.html',indexhtml)