import requests
from bs4 import BeautifulSoup

import os
import json 
import pandas as pd

# -----------------------------------------------------------------------------
def init():
    global dir_root, dir_data, dir_tmp, dir_report, dir_download
    dir_root = os.path.abspath(os.getcwd())
    createStructure()

def createStructure():
    globals()["dir_data"] = globals()["dir_root"]+'/data/'
    os.makedirs(globals()["dir_data"], exist_ok = True)

    globals()["dir_tmp"] = globals()["dir_root"]+'/tmp/'
    globals()["dir_download"] = globals()["dir_tmp"]+'/download/'
    os.makedirs(globals()["dir_download"], exist_ok = True)

    globals()["dir_report"] = globals()["dir_root"]+'/report/'
    os.makedirs(globals()["dir_report"], exist_ok = True)

# -----------------------------------------------------------------------------
def file_put_contents(filename, content,mode="w"):
    with open(filename, mode) as f_in: 
        f_in.write(content)

def file_get_contents(filename, mode="r"):
    with open(filename, mode) as f_in: 
        return f_in.read()      

# -----------------------------------------------------------------------------
def exportToCsv(data, file_path):
    ds = pd.DataFrame(data)
    ds.to_csv(file_path, index = False, header = None)

def download(url):
    file_name = os.path.basename(url)
    file_path = globals()["dir_download"]+file_name
    if not os.path.isfile(file_path) :
        r = requests.get(url)  
        file_put_contents(file_path, r.content, "wb")
    return file_path

# -----------------------------------------------------------------------------
def getMatchAction(file_path):
    content = file_get_contents(file_path)
    json_content = json.loads(content)
    
    soup = BeautifulSoup(json_content['html'], "html.parser")
    

    # Buscamos todos los elementos html del tipo LI con attributo data-gmapping
    playbyplay = soup.findAll("div", {"id" : "playbyplay"})

    items = [['score','time','action']]
    for pbp in playbyplay :
        # convertimos el json en lista
        pbpa_items = pbp.findAll("div", {"class" : "pbpa"})   
        for pbpa in pbpa_items :
            value_time = ''
            
            pbp_time_pbpsc = pbpa.find("span", {"class" : "pbpsc"})
            if pbp_time_pbpsc:
                value_score =  pbp_time_pbpsc.text
            else:
                pbp_time = pbpa.find("div", {"class" : "pbp-time"})
                value_time = pbp_time.text
            
            pbp_action = pbpa.find("div", {"class" : "pbp-action"})
            value_action = pbp_action.text

            # convertimos el json en lista
            items.append([
                value_score.strip(),
                value_time.strip(),
                value_action.strip()
            ])       

    return items

    


