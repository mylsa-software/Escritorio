import os
import json
import requests

path= os.path.dirname(os.path.abspath(__file__))
url = "http://mylsa.com.mx/pilot/DesktopRemote/Entrega.php"

data = []

with open (os.path.join(path,"Entregas.TXT"),"r") as file:
    for index,line in enumerate(file):
        valores = line.strip().split("\t")
        if index != 0 :
            data.append({"Fecha":valores[0],"Economico":valores[3],"Vin":valores[5]})

with open(os.path.join(path,"../DataUpPilot/StockPilot.json"),"r") as file:
    stock= json.load(file)

for index,dato in enumerate(data):
    flag = False
    vehiculo = None

    for vehiculoD in stock:
        if vehiculoD["vin"] == dato["Vin"]:
            vehiculo = vehiculoD
            flag = True
            break

    if flag:
        print(index)
        Send = {"Id":vehiculo["ID_vehiculos"],"fecha":dato["Fecha"],"vin":vehiculo["vin"]}
        print(Send)
        response = requests.post(url, json=Send)
        if response.status_code== 200:
            try:
                print("Respuesta JSON:", response.json())
            except Exception as e:
                print("Respuesta (texto):", response.text)
        else:
            print("Error de peticion")
        