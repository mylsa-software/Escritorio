import requests
import os
import glob
import json

def DeletSale(path):

    filestxt = glob.glob(os.path.join(path, '*.txt'))

    for file in filestxt:
        os.remove(file)

url = "http://mylsa.com.mx/pilot/DesktopRemote/Seals.php"
#url="http://localhost:8888/DesktopRemote/Seals.php"

response = requests.get(url)
path=os.path.dirname(os.path.abspath(__file__))

DeletSale(path)
InfoEconomico = []

if response.status_code == 200:
    data = response.json()

    print(data)

    for info in data:
        info['ReferenciaPilot']
        print(os.path.join(path,str(info['ReferenciaPilot'])+".txt"))
        if not os.path.exists(os.path.join(path,str(info['ReferenciaPilot'])+".txt")):
            with open(os.path.join(path,str(info['ReferenciaPilot'])+".txt"),"w") as file:
                InfoEconomico.append({"economico":info["economico"],"Cantidad":info["Cantidad a facturar"],"Venta":info["Id"],"Pilot":info['ReferenciaPilot'],"Nombre":info["NombreCliente"],"Correo":info['Correo Vendedor'],"IdPilot":info['Id']})
                for key,info in info.items():
                    file.write(key+" => " + str(info)+"\n")

    with open(os.path.join(path,"Seals.json"),"w") as file:
        file.write(json.dumps(InfoEconomico,indent=4))      
else:
    print('error de conexion')





    