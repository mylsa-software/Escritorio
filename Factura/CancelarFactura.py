import requests
import os
import json


#url="http://mylsa.com.mx/pilot/DesktopRemote/Facturado.php"
url="http://localhost/DesktopRemote/CancelarFactura.php"

path= os.path.dirname(os.path.abspath(__file__))
pathSeals = os.path.realpath(os.path.join(path,"..","ActualSeals","Seals.json"))

with open(pathSeals,"r") as file:
    dataseal = json.load(file)

datos= []

with open(os.path.join(path,"CancelarFactura.txt"),'r',encoding="latin-1") as file:
    for line in file:
        columns = line.strip().split('\t')
        datos.append(columns)

