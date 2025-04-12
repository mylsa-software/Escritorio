import requests
import os

url = "http://mylsa.com.mx/pilot/DesktopRemote/Stock.php"

response = requests.get(url)
path= os.getcwd()

if response.status_code == 200:
    data = response.json()

    print(data)

    for info in data:
        info['economico']
        print(path+"/"+info['economico']+".txt")
        if not os.path.exists(path+"/"+info['economico']+".txt"):
            with open(path+"/"+info['economico']+".txt","w") as file:
                for key,info in info.items():
                    file.write(info)
                    
else:
    print('error de conexion')