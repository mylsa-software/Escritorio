import os
import sys
import json
import requests

url="http://mylsa.com.mx/pilot/DesktopRemote/Facturado.php"

path= os.path.dirname(os.path.abspath(__file__))
pathSeals = os.path.realpath(os.path.join(path,"..","ActualSeals","Seals.json"))

with open(pathSeals,"r") as file:
    dataseal = json.load(file)

datos= []

with open(os.path.join(path,"Facturacion.txt"),'r',encoding="latin-1") as file:
    for line in file:
        columns = line.strip().split('\t')
        datos.append(columns)

with open(os.path.join(path,"Response.txt"),'w') as file:
    for row in datos:
        for index,seal in enumerate(dataseal):
            #if seal['economico'] == row[0] and seal["Cantidad"] != float(row[7]):
            #if index == 0:
            if seal['economico'] == row[0] :
                print("*"*10)
                print("IdPilot : " + seal['IdPilot'])
                print("Correo vendedor : "+ seal['Correo'])
                print("Cantidad a facturar : "+ str(seal["Cantidad"]))
                print('Nombre cliente : '+ seal['Nombre'])
                print("Folio asignado en pilot : "+ str(seal['Pilot']))
                print("UIID : "+row[8])
                print("Cantidad Facturada : "+row[7])
                print("Fecha : "+row[6])
                print("Economico : "+row[0])

                JsonSend = {
                    "tipo": "No Generico",
                    "Id":seal['IdPilot'],
                    "Folio":row[8],
                    "Fecha":row[6].replace("/", "-"),
                    "Economico":row[0],
                    "Factura":row[7]
                }

                print(JsonSend)
                respuesta = requests.post(url, json=JsonSend)
                if respuesta.status_code == 200:
                    file.write("Se subi la informacion de la factura con el economico=> "+row[0]+"\n")
                    print(respuesta.text)
                else:
                    file.write("Error de peticion => "+row[0]+"\n")
                    print('Error de peticion')
            elif len(dataseal)-1 == index:
                file.write("El economico no esta asignado a una venta en pilot activa => "+row[0]+"\n")