#!/bin/python3

# ## create graphs and pages for the live and pts json files 

# get list of files in live, pts
# loop through list creating a graph and page including the matching json file from the live/pts,json/jsonalt dirs
# super inefficent but it works.

###### make some test files in the json folders 
# they are there "just" need to write up the test

## todo
# add commandline interface
# convert from matplotlib to chartjs

import os
import pathlib
import json
import filecmp
# Using Chart.js for client-side rendering; matplotlib is no longer required

DEBUG=False
ROOT_DIR="./json"
LIVE_DIR="/Live_P64.01"
PTS_DIR="/PTS_P66.0_18Dec"
COMMON_DIR='/misc/curvetables'
SEARCH_NAME="*.json"
OUTPUT_DIR="./graphs"
INDEX_FILE="./index.html"
PTSDIRList=[]
LIVEDIRList=[]
PTSJsonaltPath = PTSJsonPath = PTSPath = PTSDIRList = LiveJsonaltPath = LiveJsonPath = LivePath = LiveDIRList = file = file1 = file2 = file3 = file4 = indexhtml = ""
all=set(())

if DEBUG :
    LIVE_DIR="/test_live"
    PTS_DIR="/test_pts"
    OUTPUT_DIR="./test_graphs"
    INDEX_FILE="./test_index.html"


def htmlheader(pagename):
    return f'''<!DOCTYPE html> <html lang="en"> 
<head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> 	
<title>{pagename}</title> 
<link rel="stylesheet" href="https://cdn.datatables.net/2.3.6/css/dataTables.dataTables.css" />
<link rel="stylesheet" href="/76CurveTables/styles.css">
<script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEv%tFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>
<script src="https://cdn.datatables.net/2.3.6/js/dataTables.js"></script> </head> <body>'''

def htmlfooter():
    return '''<script>$(document).ready( function () {
    $('#myTable').DataTable({
        paging: false
    });
} );</script> </body> </html>'''

def tablestart(col1,col2,col3,col4):
    return f'''<table id="myTable" class="display">
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
    return f'''  <tr><td>{col1}</td><td>{col2}</td><td>{col3}</td><td> {col4}</td></tr>'''

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
        # return

    # Helper to build dataset entries for Chart.js
    datasets = []
    colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']

    if file1 != '':
        title=file1.stem
        pathtmp = str(file1.parent)[str(file1.parent).find('/jsonalt')+8:]
        with open(file1, 'r') as fh:
            file1_json_data = json.load(fh)
        for entry in file1_json_data["curve"]:
            file1txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file1X.append(entry["x"])
            file1Y.append(entry["y"])
        data_points = [{"x": x, "y": y} for x,y in zip(file1X,file1Y)]
        datasets.append({"label": f"{str(PTS_DIR)[1:]} jsonAlt", "data": data_points, "borderColor": colors[0], "backgroundColor": colors[0], "tension": 0.0, "pointRadius": 3})
        file1subpagehtml+=f'<label for="ptsjsonalt">{file1}</label> <div class="box" id="ptsjsonalt">{file1txtdata}</div>'

    if file2 != '':
        title=(file2.stem)
        pathtmp = str(file2.parent)[str(file2.parent).find('/json',10)+5:]
        with open(file2, 'r') as fh:
            file2_json_data = json.load(fh)
        for entry in file2_json_data["curve"]:
            file2txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file2X.append(entry["x"])
            file2Y.append(entry["y"])
        data_points = [{"x": x, "y": y} for x,y in zip(file2X,file2Y)]
        datasets.append({"label": f"{str(PTS_DIR)[1:]} json", "data": data_points, "borderColor": colors[1], "backgroundColor": colors[1], "tension": 0.0, "pointRadius": 3})
        file2subpagehtml+=f'<label for="ptsjson">{file2}</label> <div class="box" id="ptsjson">{file2txtdata}</div>'

    if file3 != '':
        title=(file3.stem)
        pathtmp = str(file3.parent)[str(file3.parent).find('/jsonalt')+8:]
        with open(file3, 'r') as fh:
            file3_json_data = json.load(fh)
        for entry in file3_json_data["curve"]:
            file3txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file3X.append(entry["x"])
            file3Y.append(entry["y"])
        data_points = [{"x": x, "y": y} for x,y in zip(file3X,file3Y)]
        datasets.append({"label": f"{str(LIVE_DIR)[1:]} jsonAlt", "data": data_points, "borderColor": colors[2], "backgroundColor": colors[2], "tension": 0.0, "pointRadius": 3})
        file3subpagehtml+=f'<label for="Livejsonalt">{file3}</label> <div class="box" id="Livejsonalt">{file3txtdata}</div>'

    if file4 != '':
        title=(file4.stem)
        pathtmp = str(file4.parent)[str(file4.parent).find('/json',10)+5:]
        with open(file4, 'r') as fh:
            file4_json_data = json.load(fh)
        for entry in file4_json_data["curve"]:
            file4txtdata+=f'x = {entry["x"]}, y = {entry["y"]}<br>'
            file4X.append(entry["x"])
            file4Y.append(entry["y"]) 
        data_points = [{"x": x, "y": y} for x,y in zip(file4X,file4Y)]
        datasets.append({"label": f"{str(LIVE_DIR)[1:]} json", "data": data_points, "borderColor": colors[3], "backgroundColor": colors[3], "tension": 0.0, "pointRadius": 3})
        file4subpagehtml+=f'<label for="Livejson">{file4}</label> <div class="box" id="Livejson">{file4txtdata}</div>'

    # Build HTML page with Chart.js
    savePath=OUTPUT_DIR+pathtmp+"/"
    saveName=title+'.html'
    if not os.path.isdir(savePath):
        os.makedirs(savePath)

    canvas_id = f"chart_{title}"
    # Prepare JS datasets literal
    import html as _html
    def to_js_array(obj):
        # simple conversion for our data structure
        return json.dumps(obj)

    # Build the HTML using safe concatenation so JS object braces don't interfere with Python f-strings
    datasets_json = json.dumps(datasets)
    chart_html = ''
    chart_html += htmlheader(title) + "\n"
    chart_html += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n'
    chart_html += '<div style="width:900px; max-width:100%;">\n'
    chart_html += f'  <canvas id="{canvas_id}"></canvas>\n'
    chart_html += '</div>\n'
    chart_html += '<script>\n'
    chart_html += 'const datasets = ' + datasets_json + ';\n'
    chart_html += "const ctx = document.getElementById('" + canvas_id + "').getContext('2d');\n"
    chart_html += "new Chart(ctx, { type: 'line', data: { datasets: datasets }, options: { plugins: { legend: { display: true } }, scales: { x: { type: 'linear', position: 'bottom', title: { display: true, text: 'X' } }, y: { title: { display: true, text: 'Y' } } } } });\n"
    chart_html += '</script>\n'
    chart_html += '<p>\n'
    chart_html += '<table><tr><td>' + file1subpagehtml + '</td><td>' + file2subpagehtml + '</td></tr>\n'
    chart_html += '<tr><td>' + file3subpagehtml + '</td><td>' + file4subpagehtml + '</td></tr></table>\n'
    chart_html += htmlfooter() + '\n'
    writefile(savePath+saveName, chart_html)

    # detect changes between pts and live curves
    ptschanged=False
    if file1!='' and file3!='':
        if file1X!=file3X or file1Y!=file3Y:
            ptschanged=True
    if file2!='' and file4!='':
        if file2X!=file4X or file2Y!=file4Y:
            ptschanged=True
    if file2!='' and file3!='':
        if file2X!=file3X or file2Y!=file3Y:
            ptschanged=True
    if file1!='' and file4!='':
        if file1X!=file4X or file1Y!=file4Y:
            ptschanged=True
    indexhtml+=tablerow(f'<a href="{savePath+title+'.html'}">{title}</a>',ptsnew,ptsmissing,ptschanged)+'\n'
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

# Build filename->Path lookup maps (one-time) to avoid repeated rglob directory scans
def _build_name_map(pathobj):
    m = {}
    for p in pathobj.rglob(SEARCH_NAME):
        m[p.name] = p
    return m

PTS_jsonalt_map = _build_name_map(PTSJsonaltPath)
PTS_json_map = _build_name_map(PTSJsonPath)
LIVE_jsonalt_map = _build_name_map(LiveJsonaltPath)
LIVE_json_map = _build_name_map(LiveJsonPath)

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
    # want to show on the page if a flle is changed new or removed in the pts.
    # I will ignore whitespace and formatting changes.
    # 
    # i alredy have the different files looked up and will use them to test for changes.
    # i will parse the files later to make the graphs so let's use the == operator to check for changes in the parsed data.

    # PTS New is file found in PTS and not in Live
    ## if file3 and file4 not found then PTS New

    # PTS missing is file found in Live and not in PTS
    ## if file1 and file2 not found then PTS missing

    # PTS changed is file found in both and the file is changed.
    ## if file1 and file3 are found and different then PTS changed.
    ## or if file2 and file4 are found and differnet then PTS changed.

    file1 = file2 = file3 = file4 = file = ''
    ptsnew = ptsmissing = False
    # Use prebuilt lookup maps instead of re-scanning directories
    file1 = PTS_jsonalt_map.get(name, '')
    file2 = PTS_json_map.get(name, '')
    file3 = LIVE_jsonalt_map.get(name, '')
    file4 = LIVE_json_map.get(name, '')

    if file3=='' and file4=='':
        ptsnew=True

    if file1=='' and file2=='':
        ptsmissing=True

    # if file1!='' and file3!='':
    #     if not filecmp.cmp(file1,file3,shallow=False):
    #         ptschanged=True

    # if file2!='' and file4!='':
    #     if not filecmp.cmp(file2,file4,shallow=False):
    #         ptschanged=True
    makegraph()

indexhtml+=tableend()
indexhtml+=htmlfooter()
writefile(INDEX_FILE,indexhtml)
