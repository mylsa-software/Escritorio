import os
import json
import requests

url = "https://mylsa.com.mx/pilot/DesktopRemote/ActualizarDatos.php"

path=os.path.dirname(os.path.abspath(__file__))
pathStock = os.path.realpath(os.path.join(path,"..","DataUpPilot","StockPilot.json"))

with open(os.path.join(path,"CambioStock.txt"),"r") as file:
    lines = file.readlines()

with open(pathStock,"r") as file:
     Stock = json.load(file)

Info = [line.strip().split("\t") for line in lines ]

for index , row in enumerate(Info):
     for carro in Stock:
        
        if row[0] == carro["economico"]:

            JsonSend = {
            "TipoCambio":"Status",
            "Id":carro["ID_vehiculos"],
            "Status":row[1]
            }

            print(JsonSend)
            response = requests.post(url,json=JsonSend)

            if response.status_code == 200:
                print("Solicitud correcta")
            else:
                print("error")
       
