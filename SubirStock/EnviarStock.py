import json
import requests
import os

def filter (datastock,datapilot,file):

    response = []
    for stock in datastock :
        
        Exist = False

        for pilot in datapilot:
            if stock[0] == pilot["economico"]:
                
                Exist = True
                break
        
        if Exist == False:
            print(stock[0])
            response.append(stock)
        else:
                file.write("Vehiculo ya subido a pilot con el economico => " + stock[0]+"\n")  
    
    return response



url = "https://mylsa.com.mx/pilot/php/AgregarStock.php"

path=os.path.dirname(os.path.abspath(__file__))

file2 = os.path.abspath(os.path.join(path, "../PDF/Cat.json"))

file = os.path.abspath(os.path.join(path, "../PDF/Cat.json"))
filestock = os.path.abspath(os.path.join(path, "../DataUpPilot/StockPilot.json"))
txt = os.path.join(path,'stock.txt')

with open(file,'r',encoding='utf-8') as file :
    Cat = json.load(file)

with open(txt,"r", encoding="latin-1") as file:
    lines = file.readlines()

with open(filestock,"r", encoding="latin-1") as file:
    Stockpilot = json.load(file)

with open(os.path.join(path,"Response.txt"),"w",encoding="utf-8") as file:

    if Cat and Stockpilot:

        array = [line.strip().split("\t") for line in lines ]

        array = filter(array,Stockpilot,file)
        
        keys= Cat.keys()

        for index , row in enumerate(array):
            print(row)
            if index !=0:
                if row[5].split('-')[0] in keys:
                    for fo in Cat[row[5].split('-')[0]]:
                        if row[5].split('-')[1] in fo["Cat"] :
                            row.append(fo["Precio"])
                        
                
                if row[6] == 'DISPONIBLE':
                    row[6]='Disponible'
                elif row[6] == 'NO DISPONIBLE':
                    row[6]='No disponible'

                if row[7] == 'RECIBIDO':
                    row[7]='Recibido'
                elif row[7] == 'NO RECIBIDO':
                    row[7]='NoRecibido'
                
                if row[11]=="GASOLINA":
                    row[11]="0"
                elif row[11]=="DIESEL":
                    row[11]="1"
                elif row[11]=="GASLP":
                    row[11]="2"
                elif row[11]=="ELECTRICO":
                    row[11]="3"
                elif row[11]=="HIBRIDO":
                    row[11]="4"

                if row[12] == "CDMX":
                    row[12] = "DF"
                
                array[index]=row
            
        for index , row in enumerate(array):
            
            if index !=0:

                JsonSend={
                "Usuario":"Tonatiuh",
                "MarcaInput":"FORD",
                "Economico":row[0],
                "ModeloInput":row[1],
                "ColorInput":row[2],
                "YearInput":row[3],
                "VersionInput":row[4],
                "NoFabrica":row[5],
                "DisponibilidadInput":row[6],
                "SucursalInput":row[7],
                "NoPedidoInput":row[0],
                "VinInput":row[9],
                "StatusInput":row[10],
                "CombustiblesInput":row[11],
                "LocalizacionInput":row[12],
                "PrecioInput":row[13],
                "TipoVehiculo":"Nuevo"
                }

                response = requests.post(url,json=JsonSend)

                with open(os.path.join(path,"Response.txt"),"w",encoding="utf-8") as file:
                
                    if response.status_code == 200:
                        file.write(str(response.text))
                    else:
                        file.write("Error en el servicio "+str(response.status_code))                   
    else:
        print("Informacion vacia")