import requests
import os
import json

url = "http://mylsa.com.mx/pilot/DesktopRemote/Stock.php"

response = requests.get(url)
path= os.path.dirname(os.path.abspath(__file__))

if response.status_code == 200:
    data = response.json()

    #for info in data:
    #   info['economico']
    #   print(path+"/"+info['economico']+".txt")
    #   if not os.path.exists(path+"/"+info['economico']+".txt"):
    #       with open(path+"/"+info['economico']+".txt","w") as file:
    #           for key,info in info.items():
    #               file.write(info)

    with open(os.path.join(path,"StockPilot.txt"),"w") as file:
        for infodata in data:
            for key,info in infodata.items():
                file.write(str(info) + "\t")
            
            file.write("\n")

    with open(os.path.join(path,"StockPilot.json"),"w") as file:
        file.write(json.dumps(data,indent=4))
else:
    print('error de conexion')